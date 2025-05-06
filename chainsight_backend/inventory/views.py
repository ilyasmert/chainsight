from rest_framework import viewsets
from .models import (
    Ready, AtpStock, Intransit, ToBeProduced, Sales, Users
)
from .serializers import (
    ReadySerializer, AtpStockSerializer, IntransitSerializer,
    ToBeProducedSerializer, SalesSerializer, UsersSerializer
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
import pandas as pd

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