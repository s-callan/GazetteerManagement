-- SQL_LPI
SELECT
  LPI.[UPRN],
  Organisation.[OrgKey],
  LPI.[USRN],
  LPI.[PaoStartNumber],
  LPI.[PaoStartSuffix],
  LPI.[PaoEndNumber],
  LPI.[PaoEndSuffix],
  LPI.[PaoText],
  LPI.[SaoStartNumber],
  LPI.[SaoStartSuffix],
  LPI.[SaoEndNumber],
  LPI.[SaoEndSuffix],
  LPI.[SaoText],
  BLPU.[PostcodeLocator],
  Organisation.[Organisation],
  StreetDescriptor.[LocalityName],
  StreetDescriptor.[StreetDescription],
  StreetDescriptor.[TownName],
  StreetDescriptor.[AdministrativeArea],
  BLPU.[XCoordinate],
  BLPU.[YCoordinate],
  LPI.[LogicalStatus],
  LPI.[Language],
  LPI.[IS_Status]
FROM [@].[dbo].[AddressBase_LPI] AS LPI
  LEFT JOIN [@].[dbo].[AddressBase_BLPU] AS BLPU ON LPI.[UPRN] = BLPU.[UPRN]
  LEFT JOIN [@].[dbo].[AddressBase_Organisation] AS Organisation ON LPI.[UPRN] = Organisation.[UPRN]
  LEFT JOIN [@].[dbo].[AddressBase_StreetDescriptor] AS StreetDescriptor
    ON StreetDescriptor.[USRN] = LPI.[USRN] AND LPI.[Language] = StreetDescriptor.[Language]
WHERE (LPI.[IS_LastUpdated] > CONVERT(DATETIME, '#') OR
       BLPU.[IS_LastUpdated] > CONVERT(DATETIME, '#') OR
       Organisation.[IS_LastUpdated] > CONVERT(DATETIME, '#') OR
       StreetDescriptor.[IS_LastUpdated] > CONVERT(DATETIME, '#'))
      AND LPI.[LogicalStatus] IN ([~]) -- 1 - Approved, 3 - Alternative, 6 - Provisional, 8 - Historical (6,8 optional)
ORDER BY LPI.[UPRN], LPI.[LogicalStatus], CASE LPI.[Language]
                                          WHEN '|'
                                            THEN 0
                                          ELSE 1 END;
-- SQL_DPA
SELECT
  DP.[UPRN],
  DP.[RmUdprn],
  DP.[PoBoxNumber],
  DP.[OrganisationName],
  DP.[DepartmentName],
  DP.[BuildingName],
  DP.[SubBuildingName],
  DP.[BuildingNumber],
  DP.[ThoroughfareName],
  DP.[DependentThoroughfareName],
  DP.[DoubleDependentLocality],
  DP.[DependentLocality],
  DP.[PostTown],
  DP.[Postcode],
  BLPU.[XCoordinate],
  BLPU.[YCoordinate],
  DP.[WelshThoroughfareName],
  DP.[WelshDependentThoroughfareName],
  DP.[WelshDoubleDependentLocality],
  DP.[WelshDependentLocality],
  DP.[WelshPostTown]
FROM [@].[dbo].[AddressBase_DeliveryPointAddress] AS DP
  LEFT JOIN [@].[dbo].[AddressBase_BLPU] AS BLPU
    ON [DP].[UPRN] = [BLPU].[UPRN]
WHERE [DP].[IS_LastUpdated] >= CONVERT(DATETIME, '#')
ORDER BY DP.[UPRN]