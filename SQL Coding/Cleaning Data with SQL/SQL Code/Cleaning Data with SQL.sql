/* In this SQL document, we will be cleaning and transforming housing data from Nashville, TN. */


/* We will first explore the data and get familiar with it. */
SELECT * 
FROM SQLCleaning..NashVille_Data

-- At first glance, we can remove (or convert) the timestamp aspect of the SaleDate column and convert it to just a date value.

SELECT SaleDate, SaleDateClean
FROM SQLCleaning..NashVille_Data

Update SQLCleaning..NashVille_Data
SET SaleDate = CONVERT(Date, SaleDate)
-- For some reason the Update is not working. Let's try something else.

ALTER TABLE SQLCleaning..NashVille_Data
ADD SaleDateClean DATE;
Update SQLCleaning..NashVille_Data
SET SaleDateClean = CONVERT(Date, SaleDate)



/* Let's populate property address data next. But first, let's address the nulls in PropertyAddress, of which there are 29. */
SELECT PropertyAddress
FROM SQLCleaning..NashVille_Data
WHERE PropertyAddress IS NULL


-- Since we found some nulls, let's try and replace those nulls with what Addresses they should be. Firstly, I want to make sure that there aren't duplicated values which we could just paste over from. Let's see if Unique ID really is unique, and we can do this by the following query.
SELECT UniqueID, COUNT(*)
FROM SQLCleaning..NashVille_Data
GROUP BY UniqueID
HAVING COUNT(UniqueID)>1
-- Seems like the uniqueID really were all unique, so let's to fill in the address with parcel ID instead, then. Let's first verify that ParcelID does in fact repeat.
SELECT ParcelID, COUNT(*)
FROM SQLCleaning..NashVille_Data
GROUP BY ParcelID
HAVING COUNT(ParcelID)>1
-- Now knowing that ParcelID does repeat, let's try to fill in missing property addresses with that with the query and update below.

SELECT DF1.ParcelID, DF1.PropertyAddress, DF2.ParcelID, DF2.PropertyAddress, ISNULL(DF1.PropertyAddress, DF2.PropertyAddress)
FROM SQLCleaning..NashVille_Data AS DF1
INNER JOIN SQLCleaning..NashVille_Data AS DF2
	ON DF1.ParcelID = DF2.ParcelID
	AND DF1.UniqueID <> DF2.UniqueID
WHERE DF1.PropertyAddress IS NULL

UPDATE DF1
SET PropertyAddress = ISNULL(DF1.PropertyAddress, DF2.PropertyAddress)
FROM SQLCleaning..NashVille_Data AS DF1
INNER JOIN SQLCleaning..NashVille_Data AS DF2
	ON DF1.ParcelID = DF2.ParcelID
	AND DF1.UniqueID <> DF2.UniqueID
WHERE DF1.PropertyAddress IS NULL
-- Null property addresses have been filled in now :)



/* Next, let's delimit the porperty address column into three columnns (address, city, and state) */
SELECT PropertyAddress
FROM SQLCleaning..NashVille_Data 


SELECT PropertyAddress, CHARINDEX(',', PropertyAddress)
	,SUBSTRING(PropertyAddress,1,(CHARINDEX(',', PropertyAddress)-1)) AS AddressOnly
	,SUBSTRING(PropertyAddress,(CHARINDEX(',', PropertyAddress)+2), LEN(PropertyAddress)) AS CityOnly
FROM SQLCleaning..NashVille_Data

ALTER TABLE SQLCleaning..NashVille_Data
ADD AddressOnly NVARCHAR(255), CityOnly NVARCHAR(255)
UPDATE SQLCleaning..NashVille_Data
SET AddressOnly = SUBSTRING(PropertyAddress,1,(CHARINDEX(',', PropertyAddress)-1))
	,CityOnly = SUBSTRING(PropertyAddress,(CHARINDEX(',', PropertyAddress)+2), LEN(PropertyAddress))

-- Let's verify
SELECT PropertyAddress, AddressOnly, CityOnly
FROM SQLCleaning..NashVille_Data

--At this point it's a user preference, but I'm going to drop the column so I know that I've already cleaned it.
ALTER TABLE SQLCleaning..NashVille_Data
DROP COLUMN PropertyAddress
	

SELECT * FROM SQLCleaning..NashVille_Data


/* Next, let's do the same with the OwnerAddress column, but using Parsename(Replace()) */
SELECT OwnerAddress
	,PARSENAME(REPLACE(OwnerAddress, ',', '.'), 3) AS OwnerAddressClean
	,PARSENAME(REPLACE(OwnerAddress, ',', '.'), 2) AS OwnerCityClean
	,PARSENAME(REPLACE(OwnerAddress, ',', '.'), 1) AS OwnerStateClean
FROM SQLCleaning..NashVille_Data


ALTER TABLE SQLCleaning..NashVille_Data
ADD OwnerAddressClean	NVARCHAR(255)
	,OwnerCityClean		NVARCHAR(255)
	,OwnerStateClean	NVARCHAR(255)
UPDATE SQLCleaning..NashVille_Data
SET 	OwnerAddressClean	= PARSENAME(REPLACE(OwnerAddress, ',', '.'), 3)
		,OwnerCityClean		= PARSENAME(REPLACE(OwnerAddress, ',', '.'), 2)	
		,OwnerStateClean	= PARSENAME(REPLACE(OwnerAddress, ',', '.'), 1)

-- Let's verify and drop OwnerAddress column if it all checks out.
SELECT OwnerAddress, OwnerAddressClean, OwnerCityClean, OwnerStateClean
FROM SQLCleaning..NashVille_Data

ALTER TABLE SQLCleaning..NashVille_Data
DROP COLUMN OwnerAddress




/*Next up, let's convert & standarize the SoldAsVacant column to Binary values of YES/NO instead of the mix of values which are N, Yes, Y, and No. */

SELECT SoldAsVacant, COUNT(*)
FROM SQLCleaning..NashVille_Data
GROUP BY SoldAsVacant

-- For this, we can use a case statement.

SELECT DISTINCT SoldAsVacant
	,(CASE WHEN SoldAsVacant = 'N' THEN 'No'
			WHEN SoldAsVacant = 'Y' THEN 'Yes'
			ELSE SoldAsVacant END) AS SoldAsVacantClean
FROM SQLCleaning..NashVille_Data


UPDATE SQLCleaning..NashVille_Data
SET SoldAsVacant = (CASE WHEN SoldAsVacant = 'N' THEN 'No' WHEN SoldAsVacant = 'Y' THEN 'Yes' ELSE SoldAsVacant END)



/*Next, let's show how we would remove duplicates*/

WITH CTE_RowNum AS (
	SELECT *
		,ROW_NUMBER() OVER (
							PARTITION BY PARCELID
										, AddressOnly
										, SalePrice
										, SaleDateClean
										,LegalReference
										ORDER BY UniqueID) AS Rpt_Ct
	FROM SQLCleaning..NashVille_Data
	)

/* 
DELETE 
FROM CTE_RowNum 
WHERE Rpt_Ct > 1 */

SELECT * FROM CTE_RowNum WHERE Rpt_Ct > 1
