SQL_DPA = """
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
"""



class GazetteerTable(object):
    def __init__(self, name, ID, PK, config, meta=False):
        self.name = name
        self.ID = ID
        self.PK = PK
        self.config = config
        self.meta = meta
        self.PK_index = []
        self.field_index = []
        for i, field in enumerate(self.config):
            if field[0] in self.PK:
                self.PK_index.append(i)
            else:
                self.field_index.append(i)

        fields = [x[0] for x in self.config]
        if self.meta:
            fmt = "insert into %s (%s) values(%s)"
        else:
            fmt = "insert into %s (%s, Status) values(%s, 'I')"
        self.insert = fmt % (self.name, ", ".join(fields), ", ".join(["?"] * len(fields)))

        if not self.meta:
            fields = [self.config[i][0] + " = ? " for i in self.PK_index]
            self.delete = "update %s set status='D' where %s" % (self.name, "and ".join(fields))
            # print self.delete
            update = [self.config[i][0] + " = ? " for i in self.field_index]
            self.update = "update %s set status='U',%s where %s" % (self.name, ", ".join(update), "and ".join(fields))


class GazetteerDef(object):
    def __init__(self, tables):
        self.tables = tables
        self.map = {}
        for t in tables:
            if t.ID in self.map:
                print t.ID
            self.map[t.ID] = t
            # print sorted(self.map)


LAT_LONG_SIZE = 10
DATE_SIZE = 10
TIME_SIZE = 20
gazetteerDef = GazetteerDef([
    GazetteerTable(name="Header", ID="10", PK=[], meta=True,
                   config=[("CustodianName", 40),
                           ("LocalCustodianCode", 4),
                           ("ProcessData", DATE_SIZE),
                           ("VolumeNumber", 3),
                           ("EntryDate", DATE_SIZE),
                           ("TimeStamp", TIME_SIZE),
                           ("Version", 7),
                           ("FileType", 1), ]),
    GazetteerTable(name="BLPU", ID="21", PK=["UPRN"],
                   config=[  # ("ProOrder", 100),
                       ("UPRN", 12),
                       ("LogicalStatus", 1),
                       ("BlpuState", 1),
                       ("BlpuStateDate", 10),
                       ("ParentUprn", 12),
                       ("XCoordinate", 9),
                       ("YCoordinate", 10),
                       ("Latitude", LAT_LONG_SIZE),
                       ("Longitude", LAT_LONG_SIZE),
                       ("Rpc", 1),
                       ("LocalCustodianCode", 4),
                       ("Country", 1),
                       ("StartDate", 10),
                       ("EndDate", 10),
                       ("LastUpdateDate", 10),
                       ("EntryDate", 10),
                       ("PostalAddress", 1),
                       ("PostcodeLocator", 8),
                       ("MultiOccCount", 4), ]),
    GazetteerTable(name="Classification", ID="32", PK=["ClassKey"],
                   config=[  # ("ProOrder", 100),
                       ("UPRN", 12),
                       ("ClassKey", 14),
                       ("ClassificationCode", 6),
                       ("ClassScheme", 60),
                       ("SchemeVersion", 5),
                       ("StartDate", 10),
                       ("EndDate", 10),
                       ("LastUpdateDate", 10),
                       ("EntryDate", 10), ], ),
    GazetteerTable(name="DeliveryPointAddress", ID="28", PK=["UPRN"],
                   config=[  # ("ProOrder", 100),
                       ("UPRN", 12),
                       ("RmUdprn", 8),
                       ("OrganisationName", 60),
                       ("DepartmentName", 60),
                       ("SubBuildingName", 30),
                       ("BuildingName", 50),
                       ("BuildingNumber", 4),
                       ("DependentThoroughfareName", 80),
                       ("ThoroughfareName", 80),
                       ("DoubleDependentLocality", 35),
                       ("DependentLocality", 35),
                       ("PostTown", 30),
                       ("Postcode", 8),
                       ("PostcodeType", 1),
                       ("DeliveryPointSuffix", 2),
                       ("WelshDependentThoroughfareName", 80),
                       ("WelshThoroughfareName", 80),
                       ("WelshDoubleDependentLocality", 35),
                       ("WelshDependentLocality", 35),
                       ("WelshPostTown", 30),
                       ("PoBoxNumber", 6),
                       ("ProcessDate", 10),
                       ("StartDate", 10),
                       ("EndDate", 10),
                       ("LastUpdateDate", 10),
                       ("EntryDate", 10), ]),
    GazetteerTable(name="LPI", ID="24", PK=["LpiKey"],
                   config=[  # ("ProOrder", 100),
                       ("UPRN", 12),
                       ("LpiKey", 14),
                       ("Language", 3),
                       ("LogicalStatus", 1),
                       ("StartDate", 10),
                       ("EndDate", 10),
                       ("LastUpdateDate", 10),
                       ("EntryDate", 10),
                       ("SaoStartNumber", 4),
                       ("SaoStartSuffix", 2),
                       ("SaoEndNumber", 4),
                       ("SaoEndSuffix", 2),
                       ("SaoText", 90),
                       ("PaoStartNumber", 4),
                       ("PaoStartSuffix", 2),
                       ("PaoEndNumber", 4),
                       ("PaoEndSuffix", 2),
                       ("PaoText", 90),
                       ("USRN", 8),
                       ("UsrnMatchIndicator", 1),
                       ("AreaName", 35),
                       ("Level", 30),
                       ("OfficialFlag", 1), ]),
    GazetteerTable(name="Organisation", ID="31", PK=["OrgKey"],
                   config=[  # ("ProOrder", 100),
                       ("UPRN", 12),
                       ("OrgKey", 14),
                       ("Organisation", 100),
                       ("LegalName", 60),
                       ("StartDate", 10),
                       ("EndDate", 10),
                       ("LastUpdateDate", 10),
                       ("EntryDate", 10), ]),
    GazetteerTable(name="AppXRef", ID="23", PK=["XrefKey"],
                   config=[  # ("ProOrder", 100),
                       ("UPRN", 12),
                       ("XrefKey", 14),
                       ("CrossReference", 50),
                       ("Version", 3),
                       ("Source", 6),
                       ("StartDate", 10),
                       ("EndDate", 10),
                       ("LastUpdateDate", 10),
                       ("EntryDate", 10), ]),
    GazetteerTable(name="Street", ID="11", PK=["USRN"],
                   config=[  # ("ProOrder", 100),
                       ("USRN", 8),
                       ("RecordType", 1),
                       ("SwaOrgRefNaming", 4),
                       ("State", 1),
                       ("StateDate", 10),
                       ("StreetSurface", 1),
                       ("StreetClassification", 2),
                       ("Version", 3),
                       ("StreetStartDate", 10),
                       ("StreetEndDate", 10),
                       ("LastUpdateDate", 10),
                       ("RecordEntryDate", 10),
                       ("StreetStartX", 9),
                       ("StreetStartY", 10),
                       ("StreetStartLat", LAT_LONG_SIZE),
                       ("StreetStartLong", LAT_LONG_SIZE),
                       ("StreetEndX", 9),
                       ("StreetEndY", 10),
                       ("StreetEndLat", LAT_LONG_SIZE),
                       ("StreetEndLong", LAT_LONG_SIZE),
                       ("StreetTolerance", 3), ]),
    GazetteerTable(name="StreetDescriptor", ID="15", PK=["USRN"],
                   config=[  # ("ProOrder", 16),
                       ("USRN", 8),
                       ("StreetDescription", 100),
                       ("LocalityName", 35),
                       ("TownName", 30),
                       ("AdministrativeArea", 30),
                       ("Language", 3),
                       ("StartDate", DATE_SIZE),
                       ("EndDate", DATE_SIZE),
                       ("LastUpdateDate", DATE_SIZE),
                       ("EntryDate", DATE_SIZE),
                   ]),
    GazetteerTable(name="Successor", ID="30", PK=["SuccKey"],
                   config=[  # ("ProOrder", 100),
                       ("UPRN", 12),
                       ("SuccKey", 14),
                       ("StartDate", 10),
                       ("EndDate", 10),
                       ("LastUpdateDate", 10),
                       ("EntryDate", 10),
                       ("Successor", 12), ]),
    GazetteerTable(name="Metadata", ID="29", PK=[], meta=True,
                   config=[("GazName", 60),
                           ("GazScope", 60),
                           ("TerOfUse", 60),
                           ("LinkedData", 100),
                           ("GazOwner", 15),
                           ("NgazFreq", 1),
                           ("CustodianName", 40),
                           ("CustodianUprn", 12),
                           ("CustodianCode", 4),
                           ("CoOrdSystem", 40),
                           ("CoOrdUnit", 10),
                           ("MetaDate", DATE_SIZE),
                           ("ClassScheme", 60),
                           ("GazDate", DATE_SIZE),
                           ("Language", 3),
                           ("CharacterSet", 30), ]),
    GazetteerTable(name="Trailer", ID="99", PK=[], meta=True,
                   config=[("NextVolumeNumber", 3),
                           ("RecordCount", 16),
                           ("EntryDate", DATE_SIZE),
                           ("TimeStamp", TIME_SIZE), ])
])
