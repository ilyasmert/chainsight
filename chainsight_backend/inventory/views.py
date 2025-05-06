from rest_framework import viewsets
from .models import (
    Ready, AtpStock, Intransit, ToBeProduced, Sales, Users,
    ReadyArchive, AtpStockArchive, IntransitArchive, ToBeProducedArchive, SalesArchive
)
from .serializers import (
    ReadySerializer, AtpStockSerializer, IntransitSerializer,
    ToBeProducedSerializer, SalesSerializer, UsersSerializer,
    ReadyArchiveSerializer, AtpStockArchiveSerializer,
    IntransitArchiveSerializer, ToBeProducedArchiveSerializer,
    SalesArchiveSerializer
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db import connection, transaction
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from sqlalchemy import create_engine
from django.conf import settings
import io
import zipfile
from django.http import HttpResponse
import pandas as pd
from rest_framework.parsers import MultiPartParser
from .services.optimization_pipeline import OptimizationPipeline
from .services.lp_model import DEFAULT_PARAMS

def create_viewset(model, serializer):
    class GenericViewSet(viewsets.ModelViewSet):
        queryset = model.objects.all()
        serializer_class = serializer
    return GenericViewSet

ReadyViewSet = create_viewset(Ready, ReadySerializer)
AtpStockViewSet = create_viewset(AtpStock, AtpStockSerializer)
IntransitViewSet = create_viewset(Intransit, IntransitSerializer)
ToBeProducedViewSet = create_viewset(ToBeProduced, ToBeProducedSerializer)
SalesViewSet = create_viewset(Sales, SalesSerializer)

ReadyArchiveViewSet= create_viewset(ReadyArchive, ReadyArchiveSerializer)
AtpStockArchiveViewSet = create_viewset(AtpStockArchive, AtpStockArchiveSerializer)
IntransitArchiveViewSet = create_viewset(IntransitArchive, IntransitArchiveSerializer)
ToBeProducedArchiveViewSet = create_viewset(ToBeProducedArchive, ToBeProducedArchiveSerializer)
SalesArchiveViewSet = create_viewset(SalesArchive, SalesArchiveSerializer)

UsersViewSet = create_viewset(Users, UsersSerializer)

# Table mapping
ALLOWED_TABLES = {
    "ready": "ready_archive",
    "atp_stock": "atp_stock_archive",
    "intransit": "intransit_archive",
    "sales": "sales_archive",
    "to_be_produced": "to_be_produced_archive",
}

# New APIView for Excel upload and archiving
class ExcelUploadArchiveView(APIView):
    def post(self, request, *args, **kwargs):
        print("DEBUG - request.FILES:", request.FILES)
        print("DEBUG - request.POST:", request.POST)
        table = request.POST.get("tableName")
        archived_by = request.POST.get("archivedBy", "system")
        file = request.FILES.get("file")

        if not table or table not in ALLOWED_TABLES:
            return Response({"error": "Invalid or unsupported table."}, status=status.HTTP_400_BAD_REQUEST)
        if not file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Save and read Excel
            path = default_storage.save(f'temp_upload_{table}.xlsx', ContentFile(file.read()))
            file_path = default_storage.path(path)
            df = pd.read_excel(file_path)

            # Normalize column names from Excel
            df.columns = [col.lower() for col in df.columns]

            archive_table = ALLOWED_TABLES[table]
            now = timezone.now()

            with transaction.atomic():
                with connection.cursor() as cursor:
                    columns = [col.name for col in connection.introspection.get_table_description(cursor, table)]
                    columns_str = ", ".join(columns)
                    archive_columns_str = ", ".join(columns + ["archivedate", "archivedby"])

                    # Archive old data
                    cursor.execute(
                        f"INSERT INTO {archive_table} ({archive_columns_str}) "
                        f"SELECT {columns_str}, %s, %s FROM {table}",
                        [now, archived_by]
                    )

                    # Truncate current table
                    cursor.execute(f"DELETE FROM {table}")

                engine = create_engine(
                    f"postgresql+psycopg2://{settings.DATABASES['default']['USER']}:"
                    f"{settings.DATABASES['default']['PASSWORD']}@"
                    f"{settings.DATABASES['default']['HOST']}:"
                    f"{settings.DATABASES['default']['PORT']}/"
                    f"{settings.DATABASES['default']['NAME']}"
                )

                # Insert new data
                df.to_sql(table, con=engine, if_exists='append', index=False)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": f"{table} updated and archived successfully."}, status=status.HTTP_200_OK)



    """
    (.venv)(base) ~/Desktop/ceng49x/backend_integration git:[data]
        curl -X POST http://127.0.0.1:8000/api/inventory/upload-table/ \
            -F "tableName=ready" \
            -F "archivedBy=admin" \
            -F "file=@/Users/kivancfk/Desktop/ceng49x/database_azure_archive_triggers/test_data/week53/ready.xlsx"
    {"message":"ready updated and archived successfully."}%                                                                                    
    """

class UpdatePalletInfoView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file uploaded."}, status=400)

        try:
            df = pd.read_excel(file_obj)
            df.columns = df.columns.str.strip().str.lower()
            print("📊 Cleaned columns:", df.columns.tolist())

            required_cols = ['productid', 'palletcapacity', 'palletweight', 'palletused']
            if not all(col in df.columns for col in required_cols):
                return Response({
                    "error": f"Missing columns. Found: {df.columns.tolist()}"
                }, status=400)

            rows_to_insert = df[required_cols].to_numpy().tolist()
            inserted_rows = len(rows_to_insert)

            with connection.cursor() as cursor:
                cursor.execute("TRUNCATE TABLE pallet_info RESTART IDENTITY CASCADE")
                cursor.executemany("""
                    INSERT INTO pallet_info (productid, palletcapacity, palletweight, palletused)
                    VALUES (%s, %s, %s, %s)
                """, rows_to_insert)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)

        return Response({
            "status": "success",
            "inserted_rows": inserted_rows
        }, status=200)

class OptimizationRunView(APIView):
    """
    GET /api/inventory/optimize/
        ?projection_length=14&truck_per_week=2  ...etc. parameters can be passed.
    Returns a zip file named `optimization_output.zip` containing two Excel files:
    1. `optimization_results.xlsx`: Contains sheets for truck_pallets, ship_pallets,
                                     truck_m2, ship_m2, stock, and shortage.
    2. `production_suggestions.xlsx`: Contains sheets for critical_products and
                                       suggested_rearrangements.
    """
    def get(self, request, *args, **kwargs):
        # 1) Parse URL query parameters (or use defaults)
        lp_params = DEFAULT_PARAMS.copy() # Start with defaults
        for key, value in request.query_params.items():
            if key in DEFAULT_PARAMS:
                try:
                    # Attempt to convert to the type of the default parameter
                    param_type = type(DEFAULT_PARAMS[key])
                    lp_params[key] = param_type(value)
                except ValueError:
                    # Handle cases where conversion might fail, e.g., for non-integer params
                    # Or simply keep it as string if that's acceptable for some params
                    # For this example, assuming most numeric params are int as in original
                    if param_type == int:
                         lp_params[key] = int(value)
                    elif param_type == float:
                         lp_params[key] = float(value)
                    else:
                         lp_params[key] = value


        try:
            # 2) Run the optimization pipeline
            pipe = OptimizationPipeline(lp_params=lp_params)
            result = pipe.run()

            # Helper function to create an Excel file in memory from a dictionary of DataFrames
            def create_excel_in_memory(dfs_dict: dict[str, pd.DataFrame | None]) -> bytes:
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    for sheet_name, df in dfs_dict.items():
                        if isinstance(df, pd.DataFrame):
                            df.to_excel(writer, sheet_name=sheet_name, index=True)
                excel_buffer.seek(0)
                return excel_buffer.getvalue()

            # Prepare DataFrames for the first Excel file
            optimization_dfs = {
                "truck_pallets": result.get("truck_pallets"),
                "ship_pallets": result.get("ship_pallets"),
                "truck_m2": result.get("truck_m2"),
                "ship_m2": result.get("ship_m2"),
                "stock": result.get("stock"),
                "shortage": result.get("shortage"),
            }
            excel_data_optimization_bytes = create_excel_in_memory(optimization_dfs)

            # Prepare DataFrames for the second Excel file
            suggestion_dfs = {
                "critical_products": result.get("critical_products"),
                "suggested_rearrangements": result.get("suggested_rearrangements"),
            }
            excel_data_suggestions_bytes = create_excel_in_memory(suggestion_dfs)

            # Create a zip file in memory
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.writestr("optimization_results.xlsx", excel_data_optimization_bytes)
                zip_file.writestr("production_suggestions.xlsx", excel_data_suggestions_bytes)
            zip_buffer.seek(0)

            # Prepare HTTP response for the zip file
            response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="optimization_output.zip"'
            return response

        except Exception as e:
            # Log the error (e.g., import logging; logging.error(f"Error generating optimization report: {e}"))
            return Response(
                {"error": f"Failed to generate optimization report: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
