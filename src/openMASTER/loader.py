import os.path
import pandas as pd
from pyomo.environ import (
    DataPortal,
)

from openMASTER.const import (
    PATH_MODEL_IN,
    INDEX_FILENAME,
)

def load_dataportal_from_excel(filename):
    excel_to_csv(filename)
    return load_dataportal_from_csv()

def load_dataportal_from_csv() -> DataPortal:

    data = DataPortal()
    
    # Index config file path
    index_path = os.path.join(PATH_MODEL_IN, "INDEX.csv")
    
    # Loading the INDEX config
    index_config = pd.read_csv(index_path, index_col=0)
    
    # Loading Sets & Parameters to the DataPortal
    sets_and_parameters = index_config[(index_config.TYPE == "Set") | (index_config.TYPE == "Parameter")]
    
    for index, row in sets_and_parameters.iterrows():
    
        # Extracting Set & Parameters info from the INDEX Table
        sheetname = row["NAME"]
        data_type = row["TYPE"]
        dim_row   = row["DIM_ROW"]
        dim_col   = row["DIM_COL"]
        index_dim = [dim_row, dim_col]
        #print(sheetname)
        if dim_row==0 and dim_col==0:
            # Index Names
            index_names = index_config[index_config["NAME"] == sheetname]['index_names'].values[0]
        else:
            index_names = index_config[index_config["NAME"] == sheetname]['index_names'].values[0].split(",")
    
        # Loading the csv data to Data Portal
        if   data_type == "Set":
             filename = sheetname + '.csv'
             data.load(filename = os.path.join(PATH_MODEL_IN, filename), set = sheetname, format = "set")  
        elif data_type == "Parameter":
             filename = sheetname + '.csv'
             data.load(filename = os.path.join(PATH_MODEL_IN, filename), index=index_names, param=[sheetname], format="table")
    #indexed
    
    data._data[None] |= {
        'sQCEPriOUT_indexed'              : {sTE          : [(sTE,sCE)    for sCE  in data._data[None]['sCEPri'][None] if (sCE,sTE)     in data._data[None]['sQCEPriOUT'][None]] for sTE    in data._data[None]['sTE'   ][None]},
        'sQCEPriOUT_CE_indexed'           : {sCEPri       : [(sCEPri,sTE) for sTE  in data._data[None]['sTE'   ][None] if (sCEPri,sTE)  in data._data[None]['sQCEPriOUT'][None]] for sCEPri in data._data[None]['sCEPri'][None]},
        'sQCESecOUT_indexed'              : {sTE          : [(sTE,sCE)    for sCE  in data._data[None]['sCESec'][None] if (sCE,sTE)     in data._data[None]['sQCESecOUT'][None]] for sTE    in data._data[None]['sTE'   ][None]},
        'sQCESecOUT_CE_indexed'           : {sCESec       : [(sCESec,sTE) for sTE  in data._data[None]['sTE'   ][None] if (sCESec,sTE)  in data._data[None]['sQCESecOUT'][None]] for sCESec in data._data[None]['sCESec'][None]},
        'sQCEStoOUT_indexed'              : {sTE          : [(sTE,sCE)    for sCE  in data._data[None]['sCESto'][None] if (sCE,sTE)     in data._data[None]['sQCEStoOUT'][None]] for sTE    in data._data[None]['sTE'   ][None]},
        'sQCEStoOUT_CE_indexed'           : {sCESto       : [(sCESto,sTE) for sTE  in data._data[None]['sTE'   ][None] if (sCESto,sTE)  in data._data[None]['sQCEStoOUT'][None]] for sCESto in data._data[None]['sCESto'][None]},
        'sQCEPriIN_CE_indexed'            : {sCE          : [(sCE,sPE)    for sPE  in data._data[None]['sPE'   ][None] if (sPE,sCE)     in data._data[None]['sQCEPriIN' ][None]] for sCE    in data._data[None]['sCE'   ][None]},
        'sQCESecIN_CE_indexed'            : {sCE          : [(sCE,sTE)    for sTE  in data._data[None]['sTE'   ][None] if (sTE,sCE)     in data._data[None]['sQCESecIN' ][None]] for sCE    in data._data[None]['sCE'   ][None]},
        'sQCEStoIN_CE_indexed'            : {sCE          : [(sCE,sTE)    for sTE  in data._data[None]['sTE'   ][None] if (sTE,sCE)     in data._data[None]['sQCEStoIN' ][None]] for sCE    in data._data[None]['sCE'   ][None]},
        'sQCESecIN_indexed'               : {sTE          : [(sTE,sCE)    for sCE  in data._data[None]['sCESec'][None] if (sTE,sCE)     in data._data[None]['sQCESecIN' ][None]] for sTE    in data._data[None]['sTE'   ][None]},
        'sQCEStoIN_indexed'               : {sTE          : [(sTE,sCE)    for sCE  in data._data[None]['sCESto'][None] if (sTE,sCE)     in data._data[None]['sQCEStoIN' ][None]] for sTE    in data._data[None]['sTE'   ][None]},
        'sQSTOUT_indexed'                 : {sST          : [(sST,sES)    for sES  in data._data[None]['sES'   ][None] if (sST,sES)     in data._data[None]['sQSTOUT'   ][None]] for sST    in data._data[None]['sST'   ][None]},
        'sQSTInTE_indexed'                : {sST          : [(sST,sTE)    for sTE  in data._data[None]['sTE'   ][None] if (sST,sTE)     in data._data[None]['sQSTInTE'  ][None]] for sST    in data._data[None]['sST'   ][None]},
        'sVinYear_indexed'                : {sYear        : [(sYear,sVin) for sVin in data._data[None]['sVin'  ][None] if (sVin,sYear)  in data._data[None]['sVinYear'  ][None]] for sYear  in data._data[None]['sYear' ][None]},
              
        'sSTESVin_indexed'                : {(sTE, sYear) : [(sTE,sYear,sST,sES,sVin)
            for           sST                                   in data._data[None]['sST'           ][None]
            for               sES                               in data._data[None]['sES'           ][None]
            for       sVin                                      in data._data[None]['sVin'          ][None] 
              if (((  sTE,sST,sES)                              in data._data[None]['sQTESTES'      ][None]) and ((sVin,sYear) in data._data[None]['sVinYear'][None]))
                ] for sTE                                       in data._data[None]['sTE'           ][None]
                  for sYear                                     in data._data[None]['sYear'         ][None]
        },
    
        'sSTESVinTime_indexed'            : {(sTE, sYear) : [(sTE,sYear,sST,sES,sVin,sSeason,sDay,sHour)
            for  (        sST,sES)                              in data._data[None]['sQSTOUT'       ][None]
            for   sVin                                          in data._data[None]['sVin'          ][None]
            for  (sSeason,sDay,sHour)                           in data._data[None]['sSeasonDayHour'][None] 
              if (((  sTE,sST,sES)                              in data._data[None]['sQTESTES'      ][None]) and ((sVin,sYear) in data._data[None]['sVinYear'][None]))
                ] for sTE                                       in data._data[None]['sTE'           ][None]
                  for sYear                                     in data._data[None]['sYear'         ][None]
        },
    
        'sQSTVin_indexed'                 : {sYear: [(sYear,sST,sVin)
            for    sST                                          in data._data[None]['sST'           ][None]
            for    sVin                                         in data._data[None]['sVin'          ][None] 
              if ((sVin,sYear)                                  in data._data[None]['sVinYear'      ][None])
                ] for   sYear                                   in data._data[None]['sYear'         ][None]
    
        },
        'sQSTInRM_indexed'                : {sYear : [(sYear,sRM,sST,sES,sVin,sSeason,sDay,sHour)
            for  ( sRM,sST,sES)                                 in data._data[None]['sQSTInRM'      ][None]
            for    sVin                                         in data._data[None]['sVin'          ][None]
            for  ( sSeason,sDay,sHour)                          in data._data[None]['sSeasonDayHour'][None]        
              if ((sVin,sYear)                                  in data._data[None]['sVinYear'      ][None])
                ] for   sYear                                   in data._data[None]['sYear'         ][None]
                        
        },
        'sQSTOUT_VinTime_indexed'         : {sYear:[(sYear,sST,sES,sVin,sSeason,sDay,sHour)
            for  ( sST,sES)                                     in data._data[None]['sQSTOUT'       ][None]
            for    sVin                                         in data._data[None]['sVin'          ][None]
            for  ( sSeason,sDay,sHour)                          in data._data[None]['sSeasonDayHour'][None] 
              if ((sVin,sYear)                                  in data._data[None]['sVinYear'      ][None])
                ] for   sYear                                   in data._data[None]['sYear'         ][None]    
        },
        
        'sQSTOUT_ST_ES_Year_indexed'      : {(sST,sES,sYear):[(sST,sES,sYear,sVin,sSeason,sDay,sHour)
            for    sVin                                         in data._data[None]['sVin'          ][None]
            for  ( sSeason,sDay,sHour)                          in data._data[None]['sSeasonDayHour'][None] 
              if ((sVin,sYear)                                  in data._data[None]['sVinYear'      ][None])
                ] for   sYear                                   in data._data[None]['sYear'         ][None] 
                  for    sST                                    in data._data[None]['sST'           ][None] 
                  for        sES                                in data._data[None]['sES'           ][None]   
                    if ((sST,sES)                               in data._data[None]['sQSTOUT'       ][None])  
        },
    
        'sQSTOUT_STTraCar_ES_Year_indexed': {(sES_Tra,sYear):[(sES_Tra,sYear,sST_Tra_Car,sVin,sSeason,sDay,sHour)
            for     sST_Tra_Car                                 in data._data[None]['sST_Tra_Car'   ][None]
            for     sVin                                        in data._data[None]['sVin'          ][None]
            for  (  sSeason,sDay,sHour)                         in data._data[None]['sSeasonDayHour'][None] 
              if (((sST_Tra_Car,sES_Tra)                        in data._data[None]['sQSTOUT'       ][None]) and ((sVin,sYear) in data._data[None]['sVinYear'][None]))
                ] for           sES_Tra                         in data._data[None]['sES_Tra'       ][None] 
                  for sYear                                     in data._data[None]['sYear'         ][None]
        },
    
        'sQSTOUT_STTra_ES_Year_indexed'   : {(sES_Tra,sYear):[(sES_Tra,sYear,sST_Tra,sVin,sSeason,sDay,sHour)
            for     sST_Tra                                     in data._data[None]['sST_Tra'       ][None]
            for     sVin                                        in data._data[None]['sVin'          ][None]
            for  (  sSeason,sDay,sHour)                         in data._data[None]['sSeasonDayHour'][None] 
              if (((sST_Tra,sES_Tra)                            in data._data[None]['sQSTOUT'       ][None]) and ((sVin,sYear) in data._data[None]['sVinYear'][None]))
                ] for       sES_Tra                             in data._data[None]['sES_Tra'       ][None] 
                  for         sYear                             in data._data[None]['sYear'         ][None]
        },
        
        'sQSTOUT_Time_indexed'            : {sYear: [(sYear,sST,sES,sSeason,sDay,sHour)
            for (sST,sES)                                       in data._data[None]['sQSTOUT'       ][None]
            for (sSeason,sDay,sHour)                            in data._data[None]['sSeasonDayHour'][None] 
                ] for sYear                                     in data._data[None]['sYear'         ][None]
        },
    
          'sQCEPriOUT_Time_indexed'       : {sYear: [(sYear,sCE,sTE,sSeason,sDay,sHour)
            for (sCE,sTE)                                       in data._data[None]['sQCEPriOUT'    ][None]
            for (sSeason,sDay,sHour)                            in data._data[None]['sSeasonDayHour'][None] 
                ] for sYear                                     in data._data[None]['sYear'         ][None]                                                                             
          },
    
          'sQCESecOUT_Time_indexed'       : {sYear: [(sYear,sCE,sTE,sSeason,sDay,sHour)
            for (sCE,sTE)                                       in data._data[None]['sQCESecOUT'    ][None]
            for (sSeason,sDay,sHour)                            in data._data[None]['sSeasonDayHour'][None] 
                ] for sYear                                     in data._data[None]['sYear'         ][None]                                                                             
          },
    
          'sQCEStoOUT_Time_indexed'       : {sYear: [(sYear,sCE,sTE,sSeason,sDay,sHour)
            for (sCE,sTE)                                       in data._data[None]['sQCEStoOUT'    ][None]
            for (sSeason,sDay,sHour)                            in data._data[None]['sSeasonDayHour'][None] 
                ] for sYear                                     in data._data[None]['sYear'         ][None]                                                                             
          },
    
          'sQCEPriIN_indexed'             : {sPE : [(sPE,sCEPri) for sCEPri in data._data[None]['sCEPri'][None] if (sPE,sCEPri) in data._data[None]['sQCEPriIN'][None]] for sPE in data._data[None]['sPE'][None]},
    
          'sQTESTES_STES_indexed'         : {(sST,sES): [(sST,sES,sTE)
            for    sTE                                          in data._data[None]['sTE'           ][None]
              if ((sTE,sST,sES)                                 in data._data[None]['sQTESTES'      ][None])
                ] for  sST                                      in data._data[None]['sST'           ][None]
                  for      sES                                  in data._data[None]['sES'           ][None]
          },
    
          'sQSTOUT_AFTra_indexed'         : {sSD_Tra:[(sSD_Tra,sES_Tra,sST_Tra)
            for  ( sST_Tra,sES_Tra)                             in data._data[None]['sQSTOUT'       ][None]
              if ((        sES_Tra,sSD_Tra)                     in data._data[None]['sQESSD'        ][None])
                ] for              sSD_Tra                      in data._data[None]['sSD_Tra'       ][None] 
          },
    
          'sQSTOUT_AFTraCar_indexed'      : {sSD_Tra_Car:[(sSD_Tra_Car,sES_Tra,sST_Tra_Car)
            for  ( sST_Tra_Car)                                 in data._data[None]['sST_Tra_Car'][None]
            for  (             sES_Tra)                         in data._data[None]['sES_Tra'    ][None]
              if ((sST_Tra_Car,sES_Tra,sSD_Tra_Car)             in data._data[None]['sQSTESSD'   ][None])
                ] for                  sSD_Tra_Car              in data._data[None]['sSD_Tra_Car'][None] 
          },
    
          'sQSTOUT_AFTraBus_indexed'      : {sSD_Tra_Bus:[(sSD_Tra_Bus,sES_Tra,sST_Tra_Bus)
            for  ( sST_Tra_Bus)                                 in data._data[None]['sST_Tra_Bus'][None]
            for  (             sES_Tra)                         in data._data[None]['sES_Tra'    ][None]
              if ((sST_Tra_Bus,sES_Tra,sSD_Tra_Bus)             in data._data[None]['sQSTESSD'   ][None])
                ] for                  sSD_Tra_Bus              in data._data[None]['sSD_Tra_Bus'][None] 
          },
    
          'sQSTOUT_AFTraUrbRail_indexed'  : {sSD_Tra_UrbanRail:[(sSD_Tra_UrbanRail,sES_Tra,sST_Tra_UrbanRail)
            for  ( sST_Tra_UrbanRail)                           in data._data[None]['sST_Tra_UrbanRail'][None]
            for  (                    sES_Tra)                  in data._data[None]['sES_Tra'          ][None]
              if ((sST_Tra_UrbanRail,sES_Tra,sSD_Tra_UrbanRail) in data._data[None]['sQSTESSD'         ][None])
                ] for                        sSD_Tra_UrbanRail  in data._data[None]['sSD_Tra_UrbanRail'][None] 
          },
    
          'sQSTOUT_AFTraIntRail_indexed'  : {sSD_Tra_IntRail:[(sSD_Tra_IntRail,sES_Tra,sST_Tra_IntRail)
            for  ( sST_Tra_IntRail)                             in data._data[None]['sST_Tra_IntRail'  ][None]
            for  (                 sES_Tra)                     in data._data[None]['sES_Tra'          ][None]
              if ((sST_Tra_IntRail,sES_Tra,sSD_Tra_IntRail)     in data._data[None]['sQSTESSD'         ][None])
                ] for                      sSD_Tra_IntRail      in data._data[None]['sSD_Tra_IntRail'  ][None] 
          },
    
          'sQSTOUT_AFTraMoped_indexed'    : {sSD_Tra_Moped:[(sSD_Tra_Moped,sES_Tra,sST_Tra_Moped)
            for  ( sST_Tra_Moped)                               in data._data[None]['sST_Tra_Moped'    ][None]
            for  (               sES_Tra)                       in data._data[None]['sES_Tra'          ][None]
              if ((sST_Tra_Moped,sES_Tra,sSD_Tra_Moped)         in data._data[None]['sQSTESSD'         ][None])
                ] for                    sSD_Tra_Moped          in data._data[None]['sSD_Tra_Moped'    ][None] 
          },
    
          'sQSTOUT_AFTraAir_indexed'      : {sSD_Tra_Air:[(sSD_Tra_Air,sES_Tra,sST_Tra_Air)
            for  ( sST_Tra_Air)                                 in data._data[None]['sST_Tra_Air'      ][None]
            for  (             sES_Tra)                         in data._data[None]['sES_Tra'          ][None]
              if ((sST_Tra_Air,sES_Tra,sSD_Tra_Air)             in data._data[None]['sQSTESSD'         ][None])
                ] for                  sSD_Tra_Air              in data._data[None]['sSD_Tra_Air'      ][None] 
          },
    
          'sQSTOUT_AFTraSea_indexed'      : {sSD_Tra_Sea:[(sSD_Tra_Sea,sES_Tra,sST_Tra_Sea)
            for  ( sST_Tra_Sea)                                 in data._data[None]['sST_Tra_Sea'      ][None]
            for  (             sES_Tra)                         in data._data[None]['sES_Tra'          ][None]
              if ((sST_Tra_Sea,sES_Tra,sSD_Tra_Sea)             in data._data[None]['sQSTESSD'         ][None])
                ] for                  sSD_Tra_Sea              in data._data[None]['sSD_Tra_Sea'      ][None] 
          },
    
          'sQSDMD_Tra_indexed'            : {sSD_Tra     : [(sSD_Tra,sMD_Tra)     for sMD_Tra in data._data[None]['sMD_Tra'][None] if (sSD_Tra,    sMD_Tra) in data._data[None]['sQSDMD' ][None]] for sSD_Tra     in data._data[None]['sSD_Tra'    ][None]},
                 
          'sQSDMD_Tra_Car_indexed'        : {sSD_Tra_Car : [(sSD_Tra_Car,sMD_Tra) for sMD_Tra in data._data[None]['sMD_Tra'][None] if (sSD_Tra_Car,sMD_Tra) in data._data[None]['sQSDMD' ][None]] for sSD_Tra_Car in data._data[None]['sSD_Tra_Car'][None]},
            
          'sQSTOUT_AFOth_indexed'         : {sES_Oth     : [(sES_Oth,sST_Oth)     for sST_Oth in data._data[None]['sST_Oth'][None] if (sST_Oth,sES_Oth    ) in data._data[None]['sQSTOUT'][None]] for sES_Oth     in data._data[None]['sES_Oth'    ][None]},
           
          'sQSDMD_Oth_indexed'            : {sES_Oth     : [(sES_Oth,sSD_Oth,sMD_Oth)
            for  (            sSD_Oth,sMD_Oth)                  in data._data[None]['sQSDMD'           ][None]
              if ((   sES_Oth,sSD_Oth)                          in data._data[None]['sQESSD'           ][None])   
                ] for sES_Oth                                   in data._data[None]['sES_Oth'          ][None] 
          },
    
          'sQSTOUT_AFInd_indexed'         : {sSD_Ind:[(sSD_Ind,sES_Ind,sST_Ind)
            for  ( sST_Ind,sES_Ind)                             in data._data[None]['sQSTOUT'          ][None]
              if ((        sES_Ind,sSD_Ind)                     in data._data[None]['sQESSD'           ][None]) 
                ] for              sSD_Ind                      in data._data[None]['sSD_Ind'          ][None] 
          },
    
          'sQSDMD_Ind_indexed'            : {sMD_Ind : [(sMD_Ind,sSD_Ind) for sSD_Ind in data._data[None]['sSD_Ind'][None] if (sSD_Ind,sMD_Ind) in data._data[None]['sQSDMD' ][None]] for sMD_Ind in data._data[None]['sMD_Ind'][None]},
          
          'sQSTOUT_sST_Cap'               : {sST_Cap : [(sST_Cap,sES)     for sES     in data._data[None]['sES'    ][None] if (sST_Cap,sES    ) in data._data[None]['sQSTOUT'][None]] for sST_Cap in data._data[None]['sST_Cap'][None]},
          
          'sQSTOUT_sST_Uni'               : {sST_Uni : [(sST_Uni,sES,sSeason,sDay,sHour)
            for  sES                                            in data._data[None]['sES'              ][None]
            for (sSeason,sDay,sHour)                            in data._data[None]['sSeasonDayHour'   ][None] 
              if ((   sST_Uni,sES)                              in data._data[None]['sQSTOUT'          ][None]) 
                ] for sST_Uni                                   in data._data[None]['sST_Uni'          ][None]                                                                             
          }, 
    
          'sQCEPriIN_YTime_indexed'       : {(sPE,sCEPri,sYear):[(sPE,sCEPri,sYear,sSeason,sDay,sHour)
            for (sSeason,sDay,sHour)                            in data._data[None]['sSeasonDayHour'   ][None] 
              ] for    sPE                                      in data._data[None]['sPE'              ][None]
                for        sCEPri                               in data._data[None]['sCEPri'           ][None] 
                for    sYear                                    in data._data[None]['sYear'            ][None]
                  if ((sPE,sCEPri)                              in data._data[None]['sQCEPriIN'        ][None])  
          },
    
          'sQCESecIN_YTime_indexed'       : {(sTE,sCESec,sYear):[(sTE,sCESec,sYear,sSeason,sDay,sHour)
            for (sSeason,sDay,sHour)                            in data._data[None]['sSeasonDayHour'   ][None] 
              ] for    sTE                                      in data._data[None]['sTE'              ][None]
                for        sCESec                               in data._data[None]['sCESec'           ][None] 
                for    sYear                                    in data._data[None]['sYear'            ][None]
                  if ((sTE,sCESec)                              in data._data[None]['sQCESecIN'        ][None])  
          },
    
          'sQCEStoIN_YTime_indexed'       : {(sTE,sCESto,sYear):[(sTE,sCESto,sYear,sSeason,sDay,sHour)
            for (sSeason,sDay,sHour)                            in data._data[None]['sSeasonDayHour'   ][None] 
              ] for   sTE                                       in data._data[None]['sTE'              ][None]
                for        sCESto                               in data._data[None]['sCESto'           ][None] 
                for   sYear                                     in data._data[None]['sYear'            ][None]
                  if ((sTE,sCESto)                              in data._data[None]['sQCEStoIN'        ][None])  
          },  
    
          'sSTESTESVinTime_indexed'       : {(sTE,sST,sES,sYear) : [(sTE,sST,sES,sYear,sVin, sSeason, sDay, sHour)
            for     sVin                                        in data._data[None]['sVin'             ][None] 
            for  (  sSeason,sDay,sHour)                         in data._data[None]['sSeasonDayHour'   ][None] 
              if (((sVin,sYear)                                 in data._data[None]['sVinYear'         ][None]))
                ] for    sYear                                  in data._data[None]['sYear'            ][None] 
                  for    sTE                                    in data._data[None]['sTE'              ][None]
                  for        sST                                in data._data[None]['sST'              ][None]
                  for            sES                            in data._data[None]['sES'              ][None]
                    if ((sTE,sST,sES)                           in data._data[None]['sQTESTES'         ][None])
        },
    
        'sTESTESVinTime_Ele_indexed'      : {(sYear,sSeason, sDay, sHour) : [(sYear,sSeason,sDay,sHour,sTE,sST,sES,sVin)
            for    (sTE,sST,sES)                                in data._data[None]['sQTESTES_Ele'     ][None] 
            for     sVin                                        in data._data[None]['sVin'             ][None] 
              if (((sVin,sYear)                                 in data._data[None]['sVinYear'         ][None])) 
                ] for   (sYear)                                 in data._data[None]['sYear'            ][None]
                  for   (sSeason)                               in data._data[None]['sSeason'          ][None]
                  for   (sDay)                                  in data._data[None]['sDay'             ][None]
                  for   (sHour)                                 in data._data[None]['sHour'            ][None]
        },
    
    }

    return data

def excel_to_csv(excel_filepath):
    """
    Conversión archivo de datos Excel a csv.

    INPUT
    =====
    excel_filepath: Path to the Excel Input file
    csv_filepath: Path to the csv Output file

    """
    # Loading the INDEX page
    index_sheetname = "INDEX"
    index_sheet = pd.read_excel(excel_filepath, sheet_name=index_sheetname)

    # Create new columnn to store the index names
    index_sheet['index_names'] = None
    index_sheet['index_names'] = index_sheet['index_names'].astype(object)

    # Getting the names of Sets and parameters
    sets_and_parameters = index_sheet[(index_sheet.TYPE == "Set") | (index_sheet.TYPE == "Parameter")]

    for index, row in sets_and_parameters.iterrows():
        # Extracting Set & Parameters info from the INDEX Table
        sheetname = row["NAME"]
        dim_row = row["DIM_ROW"]
        dim_col = row["DIM_COL"]
        index_dim = [dim_row, dim_col]

        # Converting the Excel Table to csv
        index_names = _excel_table_to_list(excel_filepath, sheetname, index_dim)
        index_sheet.loc[index, 'index_names'] = ",".join(index_names)

    # Saving the Index Config File
    index_sheet.to_csv(INDEX_FILENAME)


def _excel_table_to_list(path, sheetname, index_dim):
    
    # Número de índices de fila
    n_row_index = index_dim[0]
    # Número de índices de columna 
    n_col_index = index_dim[1]

    # Realizamos una carga preliminar del archivo excel para determinar el comienzo y final de los datos
    raw_data = pd.read_excel(path, sheet_name = sheetname, header = None)
    # Buscamos la posición de aquellas celdas que delimiten los márgenes de los datos (KEYWORD: ~BOUNDS~)
    raw_data = pd.melt(raw_data.reset_index(), id_vars=['index'])
    is_bounds = raw_data['value'] == "~BOUNDS~"
    bounds = raw_data.loc[is_bounds, ['index', 'variable']].sort_values(['index', 'variable'])
    # Cambiamos el nombre de las columnas
    bounds.columns = ['row', 'column']

    # Extraemos los márgenes de los datos
    # Recordar que los índice de Python empiezan en 0. Si quisieramos extraer el número de fila o columna real, debemos sumarle 1 a los valores propuestos.
    start_row = min(bounds['row'])                            # Fila inicial
    end_row   = max(bounds['row'])                            # Fila final
    start_col = min(bounds['column']) + 1                     # Columna inicial
    end_col   = max(bounds['column']) - 1                     # Columna final

    # Cargamos la tabla de datos con los márgenes delimitados anteriormente
    data = pd.read_excel(path, sheet_name = sheetname, skiprows=start_row, header=list(range(0,max(1,n_col_index)))).iloc[:end_row-(start_row+max(0,n_col_index-1)),start_col:end_col+1]

    # Nombres de todos los índices
    index_names = list(data.columns[list(range(0,n_row_index))])

    # Nombres de los índices de las filas y columnas
    if n_col_index == 0:
        # Nombres de los índices de las filas
        row_index_names = index_names
        # Nombres de los índices de las columas
        col_index_names = []
    elif n_col_index == 1:
        # Nombres de los índices de las filas
        row_index_names = [name.split("/")[0].strip() for name in index_names]
        # Nombres de los índices de las columnas
        col_index_names = [index_names[0].split("/")[1].strip()]
    elif n_col_index > 1:
        # Nombres de los índices de las filas
        row_index_names = [name[-1].split("/")[0].strip() for name in index_names]
        # Nombres de los índices de las columnas
        col_index_names = [name.split("/")[0].strip() for name in index_names[0][:-1]] + [index_names[0][-1].split("/")[1].strip()]

    # Nombre de las columnas (que no son indices)
    param_column_names = list(data.columns)[n_row_index:]

    # Nombre de los Sets (indices)
    set_names = row_index_names + col_index_names

    # Si se trata de un parámetro, existirá una columna de valores
    if len(param_column_names) > 0:

        # Dataframe donde ir añadiendo los datos reformateados
        new_columns = set_names + [sheetname]
        data_list = pd.DataFrame(columns = new_columns)

        # Dataframe temporal para ir almacenando el valor de los indices y sus parametros
        # Inicializamos el Dataframe con el valor de los índices de las filas
        temp_values = pd.DataFrame(data.iloc[:,list(range(0,n_row_index))])
        temp_values.columns = temp_values.columns.to_flat_index()
        temp_values.columns = row_index_names

        # Extraemos los valores de las columnas (que no son indices)
        for i in range(len(param_column_names)):
            # Nombre de la columna actual
            current_column = param_column_names[i]
            # Extraemos SOLO la columna actual 
            current_column_values = pd.DataFrame(data[current_column])
            # Extraemos los valores de los índices de las columnas
            if n_col_index == 0:
                col_index_values = []
            elif n_col_index == 1:
                col_index_values = list(current_column_values.columns)
            elif n_col_index > 1:
                col_index_values = list(current_column_values.columns)[0] 
            # Añadimos los valores de los índices de las columnas al Dataframe temporal
            for i in range(len(col_index_values)):
                temp_values[col_index_names[i]] = col_index_values[i]
            # Añadimos el valor de los parámetros
            temp_values[sheetname] = current_column_values.values[:,0]
            # Rellenamos los valores de los parámetros vacíos con 0.0
            temp_values[sheetname].fillna(0.0, inplace = True)
            # Concatenamos los datos obtenidos a la lista de datos final (data_list)
            data_list = pd.concat([data_list, temp_values], ignore_index=True)
    
    # Si se trata de un Set, NO existirá una columna de valores
    else:
        # Creamos un Dataframe con la información de los índices del Set
        data_list = data.copy()

    # Path del fichero a exportar
    filename=sheetname+".csv"
    out_filename = os.path.join(PATH_MODEL_IN, filename)
    # Exportado de los datos en formato .csv
    os.makedirs(os.path.dirname(out_filename), exist_ok=True)
    data_list.to_csv(out_filename, index = False)

    return set_names
