# Table of Contents

- [1. Tables](#1-tables)
  - [1.1. Tables for the Current Week](#11-tables-for-the-current-week)
  - [1.2. Tables for Archived Weeks](#12-tables-for-archived-weeks)
  - [1.3. Tables for Variables](#13-tables-for-variables)
  - [1.4. Tables for General Purposes](#14-tables-for-general-purposes)
  - [1.5. Tables for the Outputs](#15-tables-for-the-outputs)
- [2. Views](#2-views)
  - [2.1. Average Sales View](#21-average-sales-view)
- [3. Triggers](#3-triggers)
  - [3.1. Ready Archive Trigger](#31-ready-archive-trigger)
  - [3.2. Sales Archive Trigger](#32-sales-archive-trigger)
  - [3.3. To Be Produced Archive Trigger](#33-to-be-produced-archive-trigger)
  - [3.4. Intransit Archive Trigger](#34-intransit-archive-trigger)
  - [3.5. Atp Stock Archive Trigger](#35-atp-stock-archive-trigger)
  - [3.6. Transportation Info Archive Trigger](#36-transportation-info-archive-trigger)
  - [3.7. Average Sales Trigger](#37-average-sales-trigger)
- [4. Tests](#4-tests)
  - [4.1. Test for Triggers per Table](#41-test-for-triggers-per-table)
  - [4.2. Test for Triggers per Views](#42-test-for-triggers-per-views)
- [5. Integrations with the Backend](#5-integrations-with-the-backend)

# 1. Tables

## 1.1. Tables for the Current Week

* **Ready**
  * productId, quantity, weekId, year
  * PRIMARY KEY (productId, weekId, year)
  
* **Sales**
  * productId, quantity, weekId, year
  * PRIMARY KEY (productId, weekId, year)
  
* **To Be Produced**
  * productId, quantity, weekId, year, ETD
  * PRIMARY KEY (productId, weekId, year, ETD)

* **Intransit**
  * productId, quantity, weekId, year, ETA
  * PRIMARY KEY (productId, weekId, year, ETA)
  
* **Atp Stock**
  * productId, quantity, weekId, year
  * PRIMARY KEY (productId, weekId, year)

## 1.2. Tables for Archived Weeks

* **Ready Archive**
  * productId, quantity, weekId, year, archiveDate, archivedBy
  * PRIMARY KEY (productId, weekId, year)
  
* **Sales Archive**
  * productId, quantity, weekId, year, archiveDate, archivedBy
  * PRIMARY KEY (productId, weekId, year)
  
* **To Be Produced Archive**
  * productId, quantity, weekId, year, ETD, archiveDate, archivedBy
  * PRIMARY KEY (productId, weekId, year, ETD)

* **Intransit Archive**
  * productId, quantity, weekId, year, ETA, archiveDate, archivedBy
  * PRIMARY KEY (productId, weekId, year, ETA)
  
* **Atp Stock Archive**
  * productId, quantity, weekId, year, archiveDate, archivedBy
  * PRIMARY KEY (productId, weekId, year)

## 1.3. Tables for Variables

* **Transportation Info**
  * transportationId, transportationName, transportationCapacity, transportationCost, year        
  * PRIMARY KEY (transportationId, year)

* **Transportation Info Archive**
  * transportationId, transportationName, transportationCapacity, transportationCost, year, archiveDate
  * PRIMARY KEY (transportationId, year, archiveDate)

* **Pallet Info**
    * productId, palletCapacity, palletWeight, palletUsed
    * PRIMARY KEY (productId)

* **Critical Products**
    * productId, isCritical,  
    * PRIMARY KEY (productId)

## 1.4. Tables for General Purposes

* **User Roles**
  * roleId, roleName
  * PRIMARY KEY (roleId)

* **Users**
  * userId, roleId, userName, password, email
  * PRIMARY KEY (userId)
  * FOREIGN KEY (roleId) REFERENCES User Roles(roleId)

## 1.5. Tables for the Outputs

    **to be completed**

# 2. Views

* **2.1. Average Sales View**

# 3. Triggers

* **3.1. Ready Archive Trigger**
* **3.2. Sales Archive Trigger**
* **3.3. To Be Produced Archive Trigger**
* **3.4. Intransit Archive Trigger**
* **3.5. Atp Stock Archive Trigger**
* **3.6. Transportation Info Archive Trigger**
* **3.7. Average Sales Trigger**

# 4. Tests

## **4.1. Test for Triggers per Table**
## **4.2. Test for Tirggers per Views**

# 5. Integrations with the Backend