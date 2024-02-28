from pyomo.environ import (
    AbstractModel,
    Set,
    Param,
    Var,
    Reals,
    NonNegativeReals,
    Objective,
    Constraint,
    minimize,
    quicksum,
)

def make_model():
    m = AbstractModel('openMASTER')
    
    m.sPE                 = Set  (                                       doc = "Primary Energy Commodities"                            )
    m.sCE                 = Set  (                                       doc = "Conversion Energy Technologies"                        )
    m.sTE                 = Set  (                                       doc = "Final Energy Commodities"                              )
    m.sRM                 = Set  (                                       doc = "Raw Materials Commodities"                             )
    m.sST                 = Set  (                                       doc = "Energy Service Supply Technologies"                    )
    m.sES                 = Set  (                                       doc = "Energy Service Commodities"                            )
    m.sSD                 = Set  (                                       doc = "Service Demand Commodities"                            )
    m.sBM                 = Set  (                                       doc = "Behavioural Measures"                                  )
    m.sDM                 = Set  (                                       doc = "Demand Shift Measures"                                 )
    m.sMD                 = Set  (                                       doc = "Macro Data"                                            )           
                 
    m.sVin                = Set  (ordered = True      ,                  doc = "Vintage years"                                         )
    m.sSeason             = Set  (ordered = True      ,                  doc = "Representative seasons/months of the year"             )
    m.sDay                = Set  (ordered = True      ,                  doc = "Representative days of the season/month"               )
    m.sHour               = Set  (ordered = True      ,                  doc = "Representative hours for a representive day"           )
    m.sSeasonDayHour      = Set  (within=m.sSeason*m.sDay*m.sHour ,      doc=  "m.sSeason*m.sDay*m.sHour"                              )
    m.sAge                = Set  (ordered = True      ,                  doc = "sAge"                                                  )
      
    #Subset  
    m.sPE_Nuc             = Set  (within=m.sPE,                          doc = "Nuclear Primary Energy Commodities"                    )
    m.sPE_Fossil          = Set  (within=m.sPE,                          doc = "Fossil Primary Energy Commodities"                     )
    m.sPE_Renew           = Set  (within=m.sPE,                          doc = "Renewable Primary Energy Commodities"                  )
                
    m.sCEPri              = Set  (within=m.sCE,                          doc = "Conversion Energy Technologies with PE input"          )
    m.sCESec              = Set  (within=m.sCE,                          doc = "Conversion Energy Technologies with TE input"          )
    m.sCESto              = Set  (within=m.sCE,                          doc = "Storage Energy Technologies"                           )
    m.sCE_Nuc             = Set  (within=m.sCE,                          doc = "Nuclear Energy Technologies"                           )
    m.sCE_Hydro           = Set  (within=m.sCE,                          doc = "Hydro Energy Technologies"                             )
    m.sCE_Coal            = Set  (within=m.sCE,                          doc = "Coal Energy Technologies"                              )
    m.sCE_Var             = Set  (within=m.sCE,                          doc = "Variable Energy Technologies"                          )
    m.sCE_Ele             = Set  (within=m.sCE,                          doc = "Electricity Energy Technologies"                       )
    m.sCE_Ref             = Set  (within=m.sCE,                          doc = "Refine Energy Technologies"                            )
      
    m.sTE_Ele             = Set  (within=m.sTE,                          doc = "Electricity Final Energy Commodities"                  )
       
    m.sST_Tra             = Set  (within=m.sST,                          doc = "Transportation Supply Technologies"                    )
    m.sModes              = Set  (                                       doc = "Transportation Modes"                                  )
    m.sST_Tra_Car         = Set  (within=m.sST,                          doc = "Transportation Supply Technologies. Car"               )
    m.sST_Tra_Air         = Set  (within=m.sST,                          doc = "Transportation Supply Technologies. Air"               )
    m.sST_Tra_Bus         = Set  (within=m.sST,                          doc = "Transportation Supply Technologies. Bus"               )
    m.sST_Tra_IntRail     = Set  (within=m.sST,                          doc = "Transportation Supply Technologies. IntRail"           )
    m.sST_Tra_Moped       = Set  (within=m.sST,                          doc = "Transportation Supply Technologies. Moped"             )
    m.sST_Tra_RoadFreight = Set  (within=m.sST,                          doc = "Transportation Supply Technologies. RoadFreight"       )
    m.sST_Tra_Sea         = Set  (within=m.sST,                          doc = "Transportation Supply Technologies. Sea"               )
    m.sST_Tra_UrbanRail   = Set  (within=m.sST,                          doc = "Transportation Supply Technologies. UrbanRail"         )
    m.sST_Oth             = Set  (within=m.sST,                          doc = "Others Supply Technologies"                            )
    m.sST_Res             = Set  (within=m.sST,                          doc = "Residential Supply Technologies"                       )
    m.sST_Ind             = Set  (within=m.sST,                          doc = "Industrial Supply Technologies"                        )
    
    m.sST_Cap             = Set  (within=m.sST,                          doc = "Supply Technologies measured by capacity units"        )
    m.sST_Uni             = Set  (within=m.sST,                          doc = "Supply Technologies measured by number of units"       ) 
    
    m.sES_Tra             = Set  (within=m.sES,                          doc = "Transportation Energy Service Commodities"             )
    m.sES_Tra_Car         = Set  (within=m.sES,                          doc = "Transportation Energy Service Commodities"             )
    m.sES_Oth             = Set  (within=m.sES,                          doc = "Others Energy Service Commodities"                     )
    m.sES_Res             = Set  (within=m.sES,                          doc = "Residential Energy Service Commodities"                )
    m.sES_Ind             = Set  (within=m.sES,                          doc = "Industrial Energy Service Commodities"                 )
    
    m.sBM_Tra             = Set  (within=m.sBM,                          doc = "Behavioural Measures in Transportation"                )
    m.sBM_Res             = Set  (within=m.sBM,                          doc = "Behavioural Measures in Others"                        )
    
    m.sDM_Tra             = Set  (within=m.sDM,                          doc = "Demand Shift Measures in Transportation"               )
    m.sDM_Res             = Set  (within=m.sDM,                          doc = "Demand Shift Measures in Others"                       )
    
    m.sSD_Tra             = Set  (within=m.sSD,                          doc = "Transportation Service Demand Commodities"             )
    m.sSD_Tra_Car         = Set  (within=m.sSD,                          doc = "Transportation Service Demand Commodities Car"         )
    m.sSD_Tra_Moped       = Set  (within=m.sSD,                          doc = "Transportation Service Demand Commodities Moped"       )
    m.sSD_Tra_Bus         = Set  (within=m.sSD,                          doc = "Transportation Service Demand Commodities Bus"         )
    m.sSD_Tra_Air         = Set  (within=m.sSD,                          doc = "Transportation Service Demand Commodities Air"         )
    m.sSD_Tra_Sea         = Set  (within=m.sSD,                          doc = "Transportation Service Demand Commodities Sea"         )
    m.sSD_Tra_UrbanRail   = Set  (within=m.sSD,                          doc = "Transportation Service Demand Commodities UrbanRail"   )
    m.sSD_Tra_IntRail     = Set  (within=m.sSD,                          doc = "Transportation Service Demand Commodities IntRail"     )
    m.sSD_Tra_RoadFreight = Set  (within=m.sSD,                          doc = "Transportation Service Demand Commodities RoadFreight" )
    m.sSD_Oth             = Set  (within=m.sSD,                          doc = "Others Service Demand Commodities"                     )
    m.sSD_Res             = Set  (within=m.sSD,                          doc = "Residential Service Demand Commodities"                )
    m.sSD_Oth_NEWB        = Set  (within=m.sSD,                          doc = "Others Service Demand Commodities. High Efficiency"    )
    m.sSD_Oth_OLDB        = Set  (within=m.sSD,                          doc = "Others Service Demand Commodities. Low  Efficiency"    )
    m.sSD_Ind             = Set  (within=m.sSD,                          doc = "Industrial Service Demand Commodities"                 )
    
    m.sMD_Tra             = Set  (within=m.sMD,                          doc = "Transportation Macro Data Commodities"                 )
    m.sMD_Res             = Set  (within=m.sMD,                          doc = "Residential Macro Data Commodities"                    )
    m.sMD_Oth             = Set  (within=m.sMD,                          doc = "Others Macro Data Commodities"                         )
    m.sMD_Ind             = Set  (within=m.sMD,                          doc = "Industrial Macro Data Commodities"                     )
      
    m.sYear               = Set  (within=m.sVin,                         doc = "Optimization years period"                             )
    m.sYearBNZ            = Set  (within=m.sVin,                         doc = "Before Net-Zero emissions target year period"          )
    m.sYearANZ            = Set  (within=m.sVin,                         doc = "After Net-Zero emissions target year period"           )
    m.sYearCoal           = Set  (within=m.sVin,                         doc = "Coal phase-out  target year period"                    )
    m.sYearNuc            = Set  (within=m.sVin,                         doc = "Nuclear dismantling target year period"                )
      
    #Relational sets  
    m.sQCEPriIN           = Set  (within=m.sPE*m.sCEPri,                 doc = "Input     PE to Primary   CE"                          )
    m.sQCESecIN           = Set  (within=m.sTE*m.sCESec,                 doc = "Input     TE to Secondary CE"                          )
    m.sQCEStoIN           = Set  (within=m.sTE*m.sCESto,                 doc = "Input     TE to Storage   CE"                          )
                                
    m.sQCEPriOUT          = Set  (within=m.sCEPri*m.sTE,                 doc = "Primary   CE to Output    TE"                          )
    m.sQCESecOUT          = Set  (within=m.sCESec*m.sTE,                 doc = "Secondary CE to Output    TE"                          )
    m.sQCEStoOUT          = Set  (within=m.sCESto*m.sTE,                 doc = "Storage   CE to Output    TE"                          )
                                
    m.sQSTInTE            = Set  (within=m.sTE*m.sST,                    doc = "Input     TE to           ST"                          )
    m.sQSTInRM            = Set  (within=m.sRM*m.sST*m.sES,              doc = "Input     RM to           ST producing ES  "           )
    m.sQSTInRM_Cir        = Set  (within=m.sRM*m.sST*m.sES,              doc = "Input     RM to           ST producing ES. Circularity")
    m.sQSTOUT             = Set  (within=m.sST*m.sES,                    doc = "          ST to Output    ES"                          )
    m.sQSTOUT_Tra         = Set  (within=m.sST_Tra*m.sES_Tra,                    doc = "          ST to Output    ES"                          )
    m.sQSTOUT_Res         = Set  (within=m.sST_Res*m.sES_Res*m.sSD_Res*m.sMD_Res,                    doc = "          ST to Output    ES"                          )
    m.sQSTOUT_Oth         = Set  (within=m.sST_Oth*m.sES_Oth,                    doc = "          ST to Output    ES"                          )
    m.sQSTOUT_Ind         = Set  (within=m.sST_Ind*m.sES_Ind,                    doc = "          ST to Output    ES"                          )
    m.sQTESTES            = Set  (within=m.sTE*m.sST*m.sES,              doc = "          TE to           ST to ES relational set"     )
    m.sQTESTES_Ele        = Set  (within=m.sTE*m.sST*m.sES,              doc = " Electr  (TE)to           ST to ES relational set"     )
    m.sQTESTES_Ind        = Set  (within=m.sTE*m.sST*m.sES,              doc = " Industry(TE)to           ST to ES relational set"     )
    m.sQESSD              = Set  (within=m.sES*m.sSD,                    doc = "          ES to           SD"                          )
    m.sQSTESSDMD_Res      = Set  (within=m.sST_Res*m.sES_Res*m.sSD_Res*m.sMD_Res,        doc = "          ST to           ES to SD to MD"              )
    m.sQSTESSD            = Set  (within=m.sST*m.sES*m.sSD,              doc = "          ST to           ES to SD"                    )
    m.sQSTESSD_Tra        = Set  (within=m.sST*m.sES*m.sSD,              doc = "          ST to           ES to SD. Transportation"    )
    m.sQESSDMD_Oth        = Set  (within=m.sES*m.sSD*m.sMD,              doc = "          ES to           SD to MD. Others"            )
    m.sQSDMD              = Set  (within=m.sSD*m.sMD,                    doc = "          SD to           MD"                          )
    m.sQSDMD_Res          = Set  (within=m.sSD*m.sMD,                    doc = "          SD to           MD"                          )
    m.sQSDMD_Oth          = Set  (within=m.sSD*m.sMD,                    doc = "          SD to           MD"                          )
    m.sQSDMD_Tra          = Set  (within=m.sSD*m.sMD,                    doc = "          SD to           MD"                          )
    
    m.sVinYear            = Set  (within=m.sVin*m.sYear,                 doc = "      Vin-Year   "                                     )
      
      
    #Specific sets  
    m.sTime               =    m.sYear*m.sSeason*m.sDay*m.sHour
    m.sVinTime            = m.sVinYear*m.sSeason*m.sDay*m.sHour
    m.sYearTime           =            m.sSeason*m.sDay*m.sHour
    m.sPEYearTime         =      m.sPE*m.sSeason*m.sDay*m.sHour
    
    #Dictionaries
    m.sQCEPriOUT_indexed               = Set(m.sTE,                             dimen=2)
    m.sQCESecOUT_indexed               = Set(m.sTE,                             dimen=2)
    m.sQCEStoOUT_indexed               = Set(m.sTE,                             dimen=2)
    m.sQCESecIN_indexed                = Set(m.sTE,                             dimen=2)
    m.sQCEStoIN_indexed                = Set(m.sTE,                             dimen=2)
    m.sSTESVin_indexed                 = Set(m.sTE, m.sYear,                    dimen=5)
    m.sSTTraESVin_indexed                 = Set(m.sTE, m.sYear,                    dimen=5)
    m.sSTOthESVin_indexed                 = Set(m.sTE, m.sYear,                    dimen=5)
    m.sSTIndESVin_indexed                 = Set(m.sTE, m.sYear,                    dimen=5)
    m.sSTResESVin_indexed                 = Set(m.sTE, m.sYear,                    dimen=5)
    m.sQSTInRM_indexed                 = Set(m.sYear,                           dimen=8)
    m.sQSTVin_indexed                  = Set(m.sYear,                           dimen=3)
    m.sQSTVinTra_indexed               = Set(m.sYear,                           dimen=3)
    m.sQSTVinOth_indexed               = Set(m.sYear,                           dimen=3)
    m.sQSTVinInd_indexed               = Set(m.sYear,                           dimen=3)
    m.sQSTVinRes_indexed               = Set(m.sYear,                           dimen=6)
    m.sQSTOUTTra_indexed               = Set(m.sYear,                           dimen=3) 
    m.sQSTOUT_VinTime_indexed          = Set(m.sYear,                           dimen=7)
    m.sQSTOUTTra_VinTime_indexed       = Set(m.sYear,                           dimen=7)
    m.sQSTOUTInd_VinTime_indexed       = Set(m.sYear,                           dimen=7)
    m.sQSTOUTRes_VinTime_indexed       = Set(m.sYear,                           dimen=9)
    m.sQSTOUTOth_VinTime_indexed       = Set(m.sYear,                           dimen=7)
    m.sQSTOUT_Time_indexed             = Set(m.sYear,                           dimen=6)
    m.sQCEPriOUT_Time_indexed          = Set(m.sYear,                           dimen=6)
    m.sQCESecOUT_Time_indexed          = Set(m.sYear,                           dimen=6)
    m.sQCEStoOUT_Time_indexed          = Set(m.sYear,                           dimen=6)
    m.sQCEPriIN_indexed                = Set(m.sPE,                             dimen=2)
    m.sQCEPriOUT_CE_indexed            = Set(m.sCEPri,                          dimen=2)
    m.sQCESecOUT_CE_indexed            = Set(m.sCESec,                          dimen=2)
    m.sQCEStoOUT_CE_indexed            = Set(m.sCESto,                          dimen=2)
    m.sQTESTES_STES_indexed            = Set(m.sST,m.sES,                       dimen=3)
    m.sQSTOUT_indexed                  = Set(m.sST,                             dimen=2)
    m.sVinYear_indexed                 = Set(m.sYear,                           dimen=2)
    m.sQSTOUT_AFTra_indexed            = Set(m.sSD_Tra,                         dimen=3)
    m.sQSDMD_Tra_indexed               = Set(m.sSD_Tra,                         dimen=2)
    m.sQSDMD_Tra_Car_indexed           = Set(m.sSD_Tra,                         dimen=2)
    m.sQSTOUT_AFOth_indexed            = Set(m.sES_Oth,                         dimen=2)
    m.sQSDMD_Oth_indexed               = Set(m.sES_Oth,                         dimen=3)
    m.sQSTOUT_AFRes_indexed            = Set(m.sES_Res,                         dimen=2)
    m.sQSDMD_Res_indexed               = Set(m.sES_Res,                         dimen=3)
    
    m.sQSTOUT_AFInd_indexed            = Set(m.sSD_Ind,                         dimen=3)
    m.sQSDMD_Ind_indexed               = Set(m.sMD_Ind,                         dimen=2)
    m.sQSTOUT_sST_Cap                  = Set(m.sST_Cap,                         dimen=2)
    m.sQSTOUT_sST_Uni                  = Set(m.sST_Uni,                         dimen=5)
    m.sQCEPriIN_YTime_indexed          = Set(m.sPE,m.sCEPri,m.sYear,            dimen=6)
    m.sQCESecIN_YTime_indexed          = Set(m.sTE,m.sCESec,m.sYear,            dimen=6)
    m.sQCEStoIN_YTime_indexed          = Set(m.sTE,m.sCESto,m.sYear,            dimen=6)
    m.sQCEPriIN_CE_indexed             = Set(m.sCE,                             dimen=2)
    m.sQCESecIN_CE_indexed             = Set(m.sCE,                             dimen=2)
    m.sQCEStoIN_CE_indexed             = Set(m.sCE,                             dimen=2)
    m.sSTESVinTime_indexed             = Set(m.sTE,m.sYear,                     dimen=8)
    m.sSTESTESVinTime_indexed          = Set(m.sTE,m.sST,m.sES,m.sYear,         dimen=8)
    m.sQSTOUT_ST_ES_Year_indexed       = Set(m.sST,m.sES,m.sYear,               dimen=7)
    m.sTESTESVinTime_Ele_indexed       = Set(m.sYear,m.sSeason,m.sDay,m.sHour,  dimen=8)
    m.sQSTOUT_STTraCar_ES_Year_indexed = Set(m.sES_Tra,m.sYear,                 dimen=7)
    m.sQSTOUT_STTra_ES_Year_indexed    = Set(m.sES_Tra,m.sYear,                 dimen=7)
    m.sQSTOUT_AFTraCar_indexed         = Set(m.sSD_Tra,                         dimen=3)
    m.sQSTOUT_AFTraBus_indexed         = Set(m.sSD_Tra,                         dimen=3)
    m.sQSTOUT_AFTraUrbRail_indexed     = Set(m.sSD_Tra,                         dimen=3)
    m.sQSTOUT_AFTraIntRail_indexed     = Set(m.sSD_Tra,                         dimen=3)
    m.sQSTOUT_AFTraMoped_indexed       = Set(m.sSD_Tra,                         dimen=3)
    m.sQSTOUT_AFTraAir_indexed         = Set(m.sSD_Tra,                         dimen=3)
    m.sQSTOUT_AFTraSea_indexed         = Set(m.sSD_Tra,                         dimen=3)
    m.sQESSDMD_Res_indexed             = Set(m.sST_Res,                         dimen=4)
    
    # Parameter definition
    m.pYr                = Param(m.sVin,                                            doc = 'Year number'                                                                                                                 )
    m.pYrGap             = Param(                                                   doc = 'Representative year gap'                                                                                                     )
    m.pTimeSlice         = Param(m.sSeason, m.sDay, m.sHour,                        doc = 'Time slice load factor'                                                                                                      )
    m.pNumHours          = Param(                                                   doc = 'Number of hours in the time slice'                                                                                           )
    m.pDisRate           = Param(                                                   doc = 'Discount Rate'                                                                                                               )
    m.pGreenfield        = Param(                                                   doc = 'GreenField=1 | BrownField=0'                                                                                                 )
    m.pEmiCO2CapSectRestr= Param(                                                   doc = 'CO2 Emission Sectorial Cap=1 | CO2 Emission Global Cap=0'                                                                    )                     
    m.pEmiCO2BudgetRestr = Param(                                                   doc = 'CO2 Emission Budget       =1 | CO2 Emission Cap       =0'                                                                    )
    m.pEmiCO2Cost        = Param(m.sYear,                                           doc = 'CO2 emission cost                                                                                    [€ per tCO2           ]')
                                    
    m.pCEResMar          = Param(                                                   doc = 'Required reserve margin over peak demand, for adequacy restriction'                                                          )
    m.pCEDemErr          = Param(                                                   doc = 'Average prediction error in demand, for reserves restriction'                                                                )
    m.pCEAFErr           = Param(                                                   doc = 'Average prediction error in CE modelled with load factors, for reserves restriction'                                         )
    m.pCEFailProb        = Param(                                                   doc = 'Larger CE failure probability to be considered for reserves restriction'                                                     )
    m.pCEFailCap         = Param(                                                   doc = 'Larger CE capacity to be considered for reserves restriction (GW of the largest plant that can fail)'                        )
                     
                     
    #Emissions                                      
                     
    ##Global emission constraints                                      
    m.pEmiCO2Budget      = Param(                                                   doc = 'CO2  emission budget'                                                                                                        )
    m.pEmiCO2Cap         = Param(m.sYear,                                           doc = 'CO2  emission cap per year'                                                                                                  )
    m.pEmiNOxCap         = Param(m.sYear,                                           doc = 'NOx  emission cap per year'                                                                                                  )
    m.pEmiSOxCap         = Param(m.sYear,                                           doc = 'SOx  emission cap per year'                                                                                                  )
    m.pEmiPM25Cap        = Param(m.sYear,                                           doc = 'PM25 emission cap per year'                                                                                                  )
    ##Sectorial CO2 constraints                             
    m.pEmiCO2CapTra      = Param(m.sYear,                                           doc = 'Transport sector            CO2 emission cap per year                                                [MtCO2                ]')
    m.pEmiCO2CapEle      = Param(m.sYear,                                           doc = 'Electricity generation      CO2 emission cap per year                                                [MtCO2                ]')
    m.pEmiCO2CapIndTE    = Param(m.sYear,                                           doc = 'Industrial sector (energy)  CO2 emission cap per year                                                [MtCO2                ]')
    m.pEmiCO2CapIndPro   = Param(m.sYear,                                           doc = 'Industrial sector (process) CO2 emission cap per year                                                [MtCO2                ]')
    m.pEmiCO2CapOth      = Param(m.sYear,                                           doc = 'Residential&Service sector  CO2 emission cap per year                                                [MtCO2                ]')
    m.pEmiCO2CapRef      = Param(m.sYear,                                           doc = 'Refinery sector             CO2 emission cap per year                                                [MtCO2                ]')
    ##CO2                                                                           
    m.pEmiCO2CEPri       = Param(m.sPE,m.sCE,                                       doc = 'Primary CE CO2 emission factor                                                                       [tCO2 per MWh         ]')
    m.pEmiCO2CESec       = Param(m.sTE,m.sCE,                                       doc = 'Secondary CE CO2 emission factor                                                                     [tCO2 per MWh         ]')
    m.pEmiCO2CESto       = Param(m.sTE,m.sCE,                                       doc = 'Storage CE CO2 emission factor                                                                       [tCO2 per MWh         ]')
    m.pEmiCO2TE          = Param(m.sTE,                                             doc = 'TE transportation CO2 emission factor                                                                [tCO2 per MWh         ]')
    m.pEmiCO2STTE        = Param(m.sST,m.sTE,                                       doc = 'TE consumption CO2 emission factor                                                                   [tCO2 per MWh         ]')
    m.pEmiCO2STPro       = Param(m.sST,m.sES,                                       doc = 'Process emission CO2 emission factor                                                                 [tCO2 per ES unit     ]')
    m.pEmiCO2ESNS        = Param(                                                   doc = 'ENS CO2 emission factor                                                                              [tCO2 per ES unit     ]')
    ##NOx                                                                                        
    m.pEmiNOxCEPri       = Param(m.sPE,m.sCE,                                       doc = 'Primary CE NOx emission factor                                                                       [tNOx per MWh         ]')
    m.pEmiNOxCESec       = Param(m.sTE,m.sCE,                                       doc = 'Secondary CE NOx emission factor                                                                     [tNOx per MWh         ]')
    m.pEmiNOxCESto       = Param(m.sTE,m.sCE,                                       doc = 'Storage CE NOx emission factor                                                                       [tNOx per MWh         ]')
    m.pEmiNOxSTTE        = Param(m.sST,m.sTE,                                       doc = 'TE consumption NOx emission factor                                                                   [tNOx per MWh         ]')
    m.pEmiNOxSTPro       = Param(m.sST,m.sES,                                       doc = 'Process emission NOx emission factor                                                                 [tNOx per ES unit     ]')
    m.pEmiNOxESNS        = Param(                                                   doc = 'ENS NOx emission factor                                                                              [tNOx per ES unit     ]')
    ##SOx                                                                                        
    m.pEmiSOxCEPri       = Param(m.sPE,m.sCE,                                       doc = 'Primary CE SOx emission factor                                                                       [tSOx per MWh         ]')
    m.pEmiSOxCESec       = Param(m.sTE,m.sCE,                                       doc = 'Secondary CE SOx emission factor                                                                     [tSOx per MWh         ]')
    m.pEmiSOxCESto       = Param(m.sTE,m.sCE,                                       doc = 'Storage CE SOx emission factor                                                                       [tSOx per MWh         ]')
    m.pEmiSOxSTTE        = Param(m.sST,m.sTE,                                       doc = 'TE consumption SOx emission factor                                                                   [tSOx per MWh         ]')
    m.pEmiSOxSTPro       = Param(m.sST,m.sES,                                       doc = 'Process emission SOx emission factor                                                                 [tSOx per ES unit     ]')
    m.pEmiSOxESNS        = Param(                                                   doc = 'ENS SOx emission factor                                                                              [tSOx per ES unit     ]')
    ##PM25                                                                                        
    m.pEmiPM25CEPri      = Param(m.sPE,m.sCE,                                       doc = 'Primary CE PM25 emission factor                                                                      [tPM25 per MWh        ]')
    m.pEmiPM25CESec      = Param(m.sTE,m.sCE,                                       doc = 'Secondary CE PM25 emission factor                                                                    [tPM25 per MWh        ]')
    m.pEmiPM25CESto      = Param(m.sTE,m.sCE,                                       doc = 'Storage CE PM25 emission factor                                                                      [tPM25 per MWh        ]')
    m.pEmiPM25STTE       = Param(m.sST,m.sTE,                                       doc = 'TE consumption PM25 emission factor                                                                  [tPM25 per MWh        ]')
    m.pEmiPM25STPro      = Param(m.sST,m.sES,                                       doc = 'Process emission PM25 emission factor                                                                [tPM25 per ES unit    ]')
    m.pEmiPM25ESNS       = Param(                                                   doc = 'ENS PM25 emission factor                                                                             [tPM25 per ES unit    ]')
                                                         
    #ESNS                                                                                                    
    m.pESNSCost          = Param(                                                   doc = 'Energy service non supplied cost                                                                     [M€ per ES unit       ]')
                                                                         
    #PE Primary Energy characterization                                                                                                                        
    m.pPECost            = Param(m.sPE,m.sYear,                                     doc = 'PE Cost                                                                                              [€    per MWh         ]')
    m.pPEDomCap          = Param(m.sPE,                                             doc = 'PE domestic consumption capacity                                                                     [GW                   ]')
    m.pPEImpCap          = Param(m.sPE,                                             doc = 'PE importation capacity                                                                              [GW                   ]')
                                                             
    #CE Conversion technologies characterization                                                                                                                                
    m.pCEOutShareMin     = Param(      m.sCE,m.sTE,                                 doc = 'Minimum Output share                                                                                 [%                    ]')
    m.pCEOutShareMax     = Param(      m.sCE,m.sTE,                                 doc = 'Maximum Output share                                                                                 [%                    ]')
    m.pSTTra_MS          = Param(      m.sModes,m.sSD,                              doc = 'Modal Shares (calibration year)                                                                      [%                    ]')
    m.pCEPriEff          = Param(m.sPE,m.sCE,                                       doc = 'CEPri Efficiency factor                                                                              [%                    ]')
    m.pCESecEff          = Param(m.sTE,m.sCE,                                       doc = 'CESec Efficiency factor                                                                              [%                    ]')
    m.pCEStoEff          = Param(m.sTE,m.sCE,                                       doc = 'CESto Efficiency factor                                                                              [%                    ]')
    m.pCELife            = Param(      m.sCE,                                       doc = 'Life of energy technologies                                                                          [years                ]')
    m.pCEInsCap          = Param(      m.sCE,                                       doc = 'Previous installed capacity of CE                                                                    [GW                   ]')
    m.pCEMaxCap          = Param(      m.sCE,                                       doc = 'Maximum installed capacity of CE                                                                     [GW                   ]')
    m.pCEStoCap          = Param(      m.sCE,                                       doc = 'Storage capacity in terms of energy                                                                  [MWh                  ]')
    m.pCECapex           = Param(      m.sCE,      m.sYear,                         doc = 'CAPEX of CE                                                                                          [€ per kW             ]')
    m.pCEDecom           = Param(      m.sCE,      m.sYear,                         doc = 'Decommission cost of CE                                                                              [€ per kW             ]')
    m.pCEFixom           = Param(      m.sCE,                                       doc = 'Fixed O&M costs of CE                                                                                [€ per kW             ]')
    m.pCEVarom           = Param(      m.sCE,m.sTE,                                 doc = 'Variable O&M costs of CE                                                                             [€ per MWh            ]')
    m.pCEReact           = Param(      m.sCE,      m.sYear,                         doc = 'Reactivation cost of CE                                                                              [€ per kW             ]')     
    m.pCEAF              = Param(      m.sCE,              m.sSeason,m.sDay,m.sHour,doc = 'Availability factor of CE                                                                            [%                    ]') 
    m.pCEFlex            = Param(      m.sCE_Ele,                                   doc = 'Electricity generation technology flexibility factor                                                 [%                    ]')
    m.pCEFirm            = Param(      m.sCE_Ele,                                   doc = 'Electricity generation technology firmness factor                                                    [%                    ]')
                                                         
    #TE Transformed energy characterization                                                                                                                                 
    m.pTELoss            = Param(m.sTE,                                             doc = 'TE transportation losses                                                                             [%                    ]')
                                                                             
    #RM Raw materials characterization                                                                                                                           
    m.pRMCost            = Param(m.sRM,m.sYear,                                     doc = 'RM cost                                                                                              [€ per ton            ]')
    m.pRMCircular        = Param(m.sES,m.sRM,                                       doc = 'RM circularity rate                                                                                  [%                    ]')
                                                                                 
    #ST technologies characterization                                                                                                                              
    m.pSTOutShareMin     = Param(m.sST,m.sES,                                       doc = 'ST Outshare minimum                                                                                  [%                    ]')
    m.pSTOutShareMax     = Param(m.sST,m.sES,                                       doc = 'ST Outshare maximum                                                                                  [%                    ]')
    m.pMSMax             = Param(                                                   doc = 'Maximum modal shift                                                                                  [%                    ]')    
    m.pTCMax             = Param(                                                   doc = 'Maximum technological choice                                                                         [%                    ]')    
    m.pSTEffTE           = Param(m.sST,m.sES,m.sTE,m.sVin,                          doc = 'ST efficiency                                                                                        [GWh per ES units     ]')
    m.pSTEffRM           = Param(m.sRM,m.sST,m.sES,                                 doc = 'RM input                                                                                             [RM units per ES units]')
    m.pSTInsCap          = Param(m.sST,m.sVin,                                      doc = 'ST previous installed capacity                                                                       [ST units             ]')        
    m.pSTMaxCap          = Param(m.sST,                                             doc = 'ST maximum allowed capacity                                                                          [ST units             ]')        
    m.pSTMaxPro          = Param(m.sST,                                             doc = 'Maximum ST annual production                                                                         [ES units             ]')
    m.pSTCapex           = Param(m.sST,m.sYear,                                     doc = 'ST CAPEX cost                                                                                        [G€ per ST unit       ]')
    m.pSTCapexRes        = Param(m.sST_Oth,m.sYear,                                 doc = 'ST CAPEX cost for residential sector                                                                 [G€ per ST unit       ]')
    m.pSTCapexInd        = Param(m.sST_Ind,m.sYear,                                 doc = 'ST CAPEX cost for industrial sector                                                                  [G€ per ST unit       ]')
    m.pSTCapexTra        = Param(m.sST_Tra,m.sYear,                                 doc = 'ST CAPEX cost for transportation sector                                                              [G€ per ST unit       ]')
    m.pSTDecom           = Param(m.sST,m.sYear,                                     doc = 'ST Decommission cost                                                                                 [G€ per ST unit       ]')
    m.pSTDecomRes        = Param(m.sST_Oth,m.sYear,                                 doc = 'ST Decommission cost for residential sector                                                          [G€ per ST unit       ]')
    m.pSTDecomInd        = Param(m.sST_Ind,m.sYear,                                 doc = 'ST Decommission cost for industrial sector                                                           [G€ per ST unit       ]')
    m.pSTDecomTra        = Param(m.sST_Tra,m.sYear,                                 doc = 'ST Decommission cost for transportation sector                                                       [G€ per ST unit       ]')
    m.pSTDecProb         = Param(m.sST,m.sAge,                                      doc = 'ST decommission probability                                                                          [%                    ]')
    m.pSTFixom           = Param(m.sST,                                             doc = 'ST Fixom cost                                                                                        [k€ per ST unit       ]') 
    m.pSTFixomRes        = Param(m.sST_Res,                                         doc = 'ST Fixom cost for residential sector                                                                 [k€ per ST unit       ]')   
    m.pSTFixomOth        = Param(m.sST_Oth,                                         doc = 'ST Fixom cost for others sector                                                                      [k€ per ST unit       ]')
    m.pSTFixomInd        = Param(m.sST_Ind,                                         doc = 'ST Fixom cost for industrial sector                                                                  [k€ per ST unit       ]')
    m.pSTFixomTra        = Param(m.sST_Tra,                                         doc = 'ST Fixom cost for transportation sector                                                              [k€ per ST unit       ]')
    m.pSTVarom           = Param(m.sST,m.sES,                                       doc = 'ST Varom cost                                                                                        [ € per ES unit       ]')         
    m.pSTVaromRes        = Param(m.sST_Res,m.sES_Res,                               doc = 'ST Varom cost for residential sector                                                                 [ € per ES unit       ]')
    m.pSTVaromOth        = Param(m.sST_Oth,m.sES_Oth,                               doc = 'ST Varom cost for others sector                                                                      [ € per ES unit       ]')
    m.pSTVaromInd        = Param(m.sST_Ind,m.sES_Ind,                               doc = 'ST Varom cost for industrial sector                                                                  [ € per ES unit       ]')
    m.pSTVaromTra        = Param(m.sST_Tra,m.sES_Tra,                               doc = 'ST Varom cost for transportation sector                                                              [ € per ES unit       ]')

    m.pESLoad            = Param(m.sES,m.sSeason,m.sDay,m.sHour,                    doc = 'ES load curve                                                                                        [%                    ]')         
    m.pESLoadTra         = Param(m.sES_Tra,m.sSeason,m.sDay,m.sHour,                    doc = 'ES load curve                                                                                        [%                    ]')         
    m.pESLoadRes         = Param(m.sES_Res,m.sSD_Res,m.sMD_Res,m.sSeason,m.sDay,m.sHour,doc = 'ES load curve                                                                                        [%                    ]')     
    m.pESLoadOth         = Param(m.sES_Oth,m.sSeason,m.sDay,m.sHour,                    doc = 'ES load curve                                                                                        [%                    ]')
    m.pESLoadInd         = Param(m.sES_Ind,m.sSeason,m.sDay,m.sHour,                    doc = 'ES load curve                                                                                        [%                    ]')
                                      
    #Activity factors                                                                                             
    m.pAFTra             = Param(m.sST,m.sES,m.sSD,                                 doc = 'Activity factor (Occupancy Rate) Transportation                                                      [%                    ]')
    m.pAFOth             = Param(m.sES,m.sSD,m.sMD,                                 doc = 'Activity factor (ES demand per dwelling/km2)                                                         [ES units             ]')
    m.pAFRes             = Param(m.sES,m.sSD,m.sMD,                                 doc = 'Activity factor (ES demand per dwelling/km2)                                                         [ES units             ]')
    m.pAFInd             = Param(m.sES,m.sSD,                                       doc = 'Activity factor (none)                                                                               [%                    ]')
    #Behavioural Measures                                                            
    m.pBMCost            = Param(m.sBM,m.sYear,                                     doc = 'Behavioural Measures Cost                                                                            [G€ per AF unit       ]')
    m.pDeltaAFTra        = Param(m.sST,m.sES,m.sSD,      m.sBM,                     doc = 'Behavioural Measures max improvement allowed (Occupancy Rate) in Transportation                      [%                    ]')
    m.pDeltaAFOth        = Param(      m.sES,m.sSD,m.sMD,m.sBM,                     doc = 'Behavioural Measures max improvement allowed (ES demand)      in Others                              [ES units             ]')
    m.pTW                = Param(      m.sES,m.sSD,m.sMD,                           doc = 'Remote work: Trade-off between residental energy service increase and transportation demand decrease [ES unit per Mpkm     ]')
    
    #Demand shit Measures
    m.pDMCost            = Param(m.sDM,m.sYear,                                     doc = 'Demand shift Measures Cost                                                                           [G€ per DC unit       ]')
    m.pDeltaDC           = Param(m.sSD,m.sMD,            m.sDM,                     doc = 'Demand shift Measures max improvement allowed                                                        [%                    ]')
    
    # Demand characterization and Macro data                                        
    m.pDC                = Param(m.sSD,m.sMD,                                       doc = 'Demand characterization                                                                              [DC unit              ]')
    m.pMD                = Param(m.sMD,m.sYear,                                     doc = 'Macro data                                                                                           [MD unit              ]')
    
    # Budget of End.Users
    m.pBudgetRes         = Param(m.sYear,                                           doc = 'Budget of Residential sector                                                                         [G€ per year          ]')
    # Variables definition
    
    #O.F. Variables
    m.vSysCost            = Var  (                                                         within = Reals,            doc = "Total System cost                                                                            [G€              ]")
    m.vTotalCost          = Var  (                                 m.sYear,                within = Reals,            doc = "Annual Total cost                                                                            [G€              ]")
    m.vBMCost             = Var  (      m.sBM,                     m.sYear,                within = Reals,            doc = "Annual Behavioural Measures cost                                                             [G€              ]")
    m.vDMCost             = Var  (      m.sDM,                     m.sYear,                within = Reals,            doc = "Annual Demand shift Measures cost                                                            [G€              ]")
    m.vPenalCost          = Var  (                                 m.sYear,                within = Reals,            doc = "Annual Penalization cost                                                                     [G€              ]")
    m.vInvCostCE          = Var  (      m.sCE,                     m.sYear,                within = Reals,            doc = "Annual Total CE investment cost                                                              [G€              ]")
    m.vInvCostST          = Var  (      m.sST,                     m.sYear,                within = Reals,            doc = "Annual Total ST investment cost                                                              [G€              ]")
    m.vOpCost             = Var  (                                 m.sYear,                within = Reals,            doc = "Annual Total operation cost                                                                  [M€              ]")
    m.vOpVarom            = Var  (                                 m.sYear,                within = Reals,            doc = "Annual Total Varom cost                                                                      [k€              ]")
    m.vInvCostSTRes       = Var  (      m.sST_Res, m.sES_Res,m.sSD_Res, m.sMD_Res,m.sYear, within = Reals,            doc = "Annual Total ST investment cost for residential sector                                       [G€              ]") 
    m.vInvCostSTOth       = Var  (      m.sST_Oth,                 m.sYear,                within = Reals,            doc = "Annual Total ST investment cost for residential sector                                       [G€              ]")
    m.vInvCostSTInd       = Var  (      m.sST_Ind,                 m.sYear,                within = Reals,            doc = "Annual Total ST investment cost for industrial sector                                        [G€              ]")
    m.vInvCostSTTra       = Var  (      m.sST_Tra,                 m.sYear,                within = Reals,            doc = "Annual Total ST investment cost for transportation sector                                    [G€              ]")               
                                    
    #Origin of PE - variables                                 
    m.vQPEDom             = Var  (m.sPE,                           m.sTime,                within = NonNegativeReals, doc = "PE domestic consumption                                                                      [GWh             ]")
    m.vQPEImp             = Var  (m.sPE,                           m.sTime,                within = NonNegativeReals, doc = "PE imports                                                                                   [GWh             ]")
                            
    #CE conversion technologies using PE commodities - var       iables                       
    m.vQCEPriIN           = Var  (      m.sQCEPriIN,               m.sTime,                within = NonNegativeReals, doc = "PE consumed by CE techs                                                                      [GWh             ]")
    m.vQCEPriOUT          = Var  (      m.sQCEPriOUT,              m.sTime,                within = NonNegativeReals, doc = "TE produced in CE techs from PE energy                                                       [GWh             ]")
                            
    #CE conversion technologies using TE commodities - var       iables                     
    m.vQCESecIN           = Var  (      m.sQCESecIN,               m.sTime,                within = NonNegativeReals, doc = "TE consumed by CE techs                                                                      [GWh             ]")
    m.vQCESecOUT          = Var  (      m.sQCESecOUT,              m.sTime,                within = NonNegativeReals, doc = "TE produced in CE techs from TE energy                                                       [GWh             ]")    
                            
    #Storage technologies using TE commodities - variables                         
    m.vQCEStoIN           = Var  (      m.sQCEStoIN,               m.sTime,                within = NonNegativeReals, doc = "TE stored by Storage techs")                  
    m.vQCEStoOUT          = Var  (      m.sQCEStoOUT,              m.sTime,                within = NonNegativeReals, doc = "TE released in Storage techs from TE energy                                                  [GWh             ]")    
                            
    m.vCEStoLevel         = Var  (      m.sCESto,                  m.sTime,                within = NonNegativeReals, doc = "Accumulated energy stored in Storage processes                                               [GWh             ]")
                            
    #TE transport energy losses - variables                         
    m.vQTELoss            = Var  (      m.sTE,                     m.sTime,                within = NonNegativeReals, doc = "TE losses in transportation processes                                                        [GWh             ]")
                            
    #ST balance - variables                         
    m.vQSTInTE            = Var  (           m.sQTESTES,           m.sVinTime,             within = NonNegativeReals, doc = "TE consumed by ST                                                                            [GWh             ]")
    m.vQSTTraInTE
    m.vQSTInRM            = Var  (           m.sQSTInRM,           m.sVinTime,             within = NonNegativeReals, doc = "RM consumed by ST (industrial)                                                               [Tons            ]")
    m.vQSTOut             = Var  (           m.sQSTOUT,            m.sVinTime,             within = NonNegativeReals, doc = "ES produced by ST                                                                            [ES units        ]")
    m.vQSTOut_Res         = Var  (           m.sQSTESSDMD_Res,     m.sVinTime,             within = NonNegativeReals, doc = "ES produced by ST for residential sector                                                     [ES units        ]")
    m.vQSTOut_Ind         = Var  (           m.sQSTOUT,            m.sVinTime,             within = NonNegativeReals, doc = "ES produced by ST for industrial sector                                                      [ES units        ]")
    m.vQSTOut_Tra         = Var  (           m.sQSTOUT,            m.sVinTime,             within = NonNegativeReals, doc = "ES produced by ST for transportation sector                                                  [ES units        ]")
    m.vQSTOut_Oth         = Var  (           m.sQSTOUT,            m.sVinTime,             within = NonNegativeReals, doc = "ES produced by ST for others                                                                 [ES units        ]")

    #ES                              
    m.vQESNS              = Var  (           m.sQSTOUT,            m.sTime,                within = NonNegativeReals, doc = "ES not supplied (slack variable)                                                             [ES units        ]")
    m.vQES                = Var  (           m.sQSTOUT,            m.sYear,                within = NonNegativeReals, doc = "ES                                                                                           [ES units        ]")
    m.vQES_Res            = Var  (           m.sQSTESSDMD_Res,     m.sYear,                within = NonNegativeReals, doc = "ES for residential sector                                                                     [ES units        ]")
    m.vQES_Ind            = Var  (           m.sQSTOUT,            m.sYear,                within = NonNegativeReals, doc = "ES for industrial sector                                                                      [ES units        ]")
    m.vQES_Tra            = Var  (           m.sQSTOUT,            m.sYear,                within = NonNegativeReals, doc = "ES for transportation sector                                                                  [ES units        ]")
    m.vQES_Oth            = Var  (           m.sQSTESSDMD_Oth,     m.sYear,                within = NonNegativeReals, doc = "ES for others                                                                                 [ES units        ]")

    #BM
    m.vBMTra              = Var  (        m.sQSTESSD_Tra,m.sBM_Tra,m.sYear,                within = NonNegativeReals, doc = "Behavioural Measures. Transportation                                                         [ES units        ]")
    m.vBMRes              = Var  (        m.sQESSDMD_Res,m.sBM_Res,m.sYear,                within = NonNegativeReals, doc = "Behavioural Measures. Others                                                                 [ES units        ]")
    m.vBMRes_WAMAC        = Var  (          m.sQSDMD_Res,m.sBM_Res,m.sYear,                within = NonNegativeReals, doc = "Behavioural Measures. Others. Cold cycle Washing Machine                                     [ES units        ]")
    m.vBMRes_DIWAC        = Var  (          m.sQSDMD_Res,m.sBM_Res,m.sYear,                within = NonNegativeReals, doc = "Behavioural Measures. Others. Cold cycle Dish Washer                                         [ES units        ]")
    m.vBMRes_TW           = Var  (        m.sQESSDMD_Res,          m.sYear,                within = NonNegativeReals, doc = "Behavioural Measures. Others. Telework                                                       [ES units        ]")
    
    #SD                    
    m.vQSDTra             = Var  (           m.sSD_Tra,            m.sYear,                within = NonNegativeReals, doc = "Transportation SD                                                                            [SD units        ]")
    m.vQSDRes             = Var  (           m.sSD_Res,m.sMD_Res,  m.sYear,                within = NonNegativeReals, doc = "Others SD                                                                                    [SD units        ]")
    m.vQSDInd             = Var  (           m.sSD_Ind,            m.sYear,                within = NonNegativeReals, doc = "Industrial SD                                                                                [SD units        ]")
    m.vQSDOth             = Var  (           m.sSD_Oth,m.sMD_Oth,  m.sYear,                within = NonNegativeReals, doc = "Residential SD                                                                               [SD units        ]")
    #DM
    m.vDMTra              = Var  (        m.sQSDMD_Tra,m.sDM_Tra,m.sYear,                  within = NonNegativeReals, doc = "DMTra                                                                                        [SD units        ]")
    m.vDMOth_HE           = Var  (        m.sMD_Oth,   m.sDM_Oth,m.sYear,                  within = NonNegativeReals, doc = "DMOth_HE                                                                                     [SD units        ]")                 
    m.vDMOth_LE           = Var  (        m.sMD_Oth,   m.sDM_Oth,m.sYear,                  within = NonNegativeReals, doc = "DMOth_LE                                                                                     [SD units        ]")                 
    
    
    #CE capacity variables                  
    m.vCENewCap           = Var  (      m.sCE,                     m.sYear,                within = NonNegativeReals, doc = "CE new installed capacity                                                                    [GW              ]")
    m.vCETotCap           = Var  (      m.sCE,                     m.sYear,                within = NonNegativeReals, doc = "CE accumulated installed capacity                                                            [GW              ]")
    m.vCEDecCap           = Var  (      m.sCE,                     m.sYear,                within = NonNegativeReals, doc = "CE decommisioned capacity                                                                    [GW              ]")
    m.vCEActCap           = Var  (      m.sCE,                     m.sYear,                within = NonNegativeReals, doc = "Active CE capacity                                                                           [GW              ]")
    m.vCEHibCap           = Var  (      m.sCE,                     m.sYear,                within = NonNegativeReals, doc = "CE capacity in hibernation                                                                   [GW              ]")
    m.vCEDeltaActCap      = Var  (      m.sCE,                     m.sYear,                within = NonNegativeReals, doc = "Reactivation of CE inactive capacity                                                         [GW              ]")
    
    m.vCEEleReserv        = Var  (      m.sCE_Ele,                 m.sTime,                within = NonNegativeReals, doc = "CE electricity reserves                                                                      [GW              ]")
    m.vEleMaxDem          = Var  (                                 m.sYear,                within = NonNegativeReals, doc = "Yearly maximum electricity demand in a time slice                                            [GW              ]")
    
    
    #ST capacity variables                          
    m.vSTNewCap           = Var  (      m.sST,                     m.sYear,                within = NonNegativeReals, doc = "ST new installed capacity                                                                    [GW              ]")
    m.vSTNewCapRes        = Var  (m.sES_Res,m.sMD_Res, m.sSD_Res,      m.sST_Res,                 m.sYear,                within = NonNegativeReals, doc = "ST new installed capacity for residential sector                                             [GW              ]")
    m.vSTNewCapOth        = Var  (      m.sST_Oth,                 m.sYear,                within = NonNegativeReals, doc = "ST new installed capacity for others sector                                                  [GW              ]")
    m.vSTNewCapInd        = Var  (      m.sST_Ind,                 m.sYear,                within = NonNegativeReals, doc = "ST new installed capacity for industrial sector                                              [GW              ]")
    m.vSTNewCapTra        = Var  (      m.sST_Tra,                 m.sYear,                within = NonNegativeReals, doc = "ST new installed capacity for transportation sector                                          [GW              ]")
    m.vSTDecCap           = Var  (      m.sST,      m.sVinYear,                            within = NonNegativeReals, doc = "ST decommissioned capacity                                                                   [GW              ]")
    m.vSTDecCapRes        = Var  (m.ES_Res,m.sMD_Res, m.sSD_Res,      m.sST_Res,  m.sVinYear,                            within = NonNegativeReals, doc = "ST decommissioned capacity for residential sector                                            [GW              ]")
    m.vSTDecCapInd        = Var  (      m.sST_Ind,  m.sVinYear,                            within = NonNegativeReals, doc = "ST decommissioned capacity for industrial sector                                             [GW              ]")
    m.vSTDecCapTra        = Var  (      m.sST_Tra,  m.sVinYear,                            within = NonNegativeReals, doc = "ST decommissioned capacity for transportation sector                                         [GW              ]")
    m.vSTDecCapOth        = Var  (      m.sST_Oth,  m.sVinYear,                            within = NonNegativeReals, doc = "ST decommissioned capacity for others sector                                                  [GW              ]")
    m.vSTTotCap           = Var  (      m.sST,      m.sVinYear,                            within = NonNegativeReals, doc = "ST accumulated installed capacity                                                            [GW              ]")
    m.vSTTotCapTra        = Var  (      m.sST_Tra,  m.sVinYear,                            within = NonNegativeReals, doc = "ST accumulated installed capacity for transportation sector                                  [GW              ]")
    m.vSTTotCapRes        = Var  (      m.sST_Res,  m.sVinYear,                            within = NonNegativeReals, doc = "ST accumulated installed capacity for residential sector                                     [GW              ]")
    m.vSTTotCapInd        = Var  (      m.sST_Ind,  m.sVinYear,                            within = NonNegativeReals, doc = "ST accumulated installed capacity for industrial sector                                      [GW              ]")
    m.vSTTotCapOth        = Var  (      m.sST_Oth,  m.sVinYear,                            within = NonNegativeReals, doc = "ST accumulated installed capacity for others sector                                           [GW              ]")
    m.vInvUserRes         = Var  (m.sMD_Oth,m.sSD_Oth,                                 m.sYear,                within = NonNegativeReals, doc = "Annual investment of residential sector                                                      [G€              ]")  

    #CO2 Emission variables                               
    m.vEmiCO2CE           = Var  (      m.sCE,                     m.sYear,                within = NonNegativeReals, doc = "CO2 emissions produced in CE processes                                                       [ktCO2           ]")
    m.vEmiCO2CEPri        = Var  (m.sQCEPriIN,                     m.sYear,                within = NonNegativeReals, doc = "CO2 emissions produced in Primary CE processes                                               [ktCO2           ]")
    m.vEmiCO2CESec        = Var  (m.sQCESecIN,                     m.sYear,                within = NonNegativeReals, doc = "CO2 emissions produced in Secondary CE processes                                             [ktCO2           ]")
    m.vEmiCO2CESto        = Var  (m.sQCEStoIN,                     m.sYear,                within = NonNegativeReals, doc = "CO2 emissions produced in Storage CE processes                                               [ktCO2           ]")
    m.vEmiCO2TE           = Var  (            m.sTE,               m.sYear,                within = NonNegativeReals, doc = "CO2 emissions produced in the transportation of TE                                           [ktCO2           ]")
    m.vEmiCO2STTE         = Var  (            m.sQTESTES,          m.sYear,                within = NonNegativeReals, doc = "CO2 emissions produced in ST due to TE consumption                                           [ktCO2           ]")
    m.vEmiCO2STPro        = Var  (                  m.sQSTOUT,     m.sYear,                within = NonNegativeReals, doc = "CO2 emissions produced in ST due to activity processes                                       [ktCO2           ]")
    m.vEmiCO2ST           = Var  (                  m.sQSTOUT,     m.sYear,                within = NonNegativeReals, doc = "CO2 emissions produced in ST                                                                 [ktCO2           ]")
    m.vEmiCO2ESNS         = Var  (                                 m.sYear,                within = NonNegativeReals, doc = "CO2 emissions related to ESNS                                                                [ktCO2           ]")
    m.vEmiCO2Tot          = Var  (                                 m.sYear,                within = NonNegativeReals, doc = "Annual Total CO2 emissions                                                                   [MtCO2           ]")
    m.vEmiCO2CapExc       = Var  (                                 m.sYear,                within = NonNegativeReals, doc = "Excess of CO2 emissions regarding Carbon Cap 2050 onwards (slack variable)                   [MtCO2           ]")
    m.vEmiCO2BudgetExc    = Var  (                                                         within = NonNegativeReals, doc = "Excess of CO2 emissions regarding Carbon Budget (slack variable)                             [MtCO2           ]")
                    
    #NOx Emission variables                               
    m.vEmiNOxCE           = Var  (      m.sCE,                     m.sYear,                within = NonNegativeReals, doc = "NOx emissions produced in CE processes                                                       [ktNOx           ]")
    m.vEmiNOxCEPri        = Var  (m.sQCEPriIN,                     m.sYear,                within = NonNegativeReals, doc = "NOx emissions produced in Primary CE processes                                               [ tNOx           ]")
    m.vEmiNOxCESec        = Var  (m.sQCESecIN,                     m.sYear,                within = NonNegativeReals, doc = "NOx emissions produced in Secondary CE processes                                             [ tNOx           ]")
    m.vEmiNOxCESto        = Var  (m.sQCEStoIN,                     m.sYear,                within = NonNegativeReals, doc = "NOx emissions produced in Storage CE processes                                               [ tNOx           ]")
    m.vEmiNOxSTTE         = Var  (            m.sQTESTES,          m.sYear,                within = NonNegativeReals, doc = "NOx emissions produced in ST due to TE consumption                                           [ tNOx           ]")
    m.vEmiNOxSTPro        = Var  (                  m.sQSTOUT,     m.sYear,                within = NonNegativeReals, doc = "NOx emissions produced in ST due to activity processes                                       [ tNOx           ]")
    m.vEmiNOxST           = Var  (                  m.sQSTOUT,     m.sYear,                within = NonNegativeReals, doc = "NOx emissions produced in ST                                                                 [ktNOx           ]")
    m.vEmiNOxESNS         = Var  (                                 m.sYear,                within = NonNegativeReals, doc = "NOx emissions related to ESNS                                                                [ktNOx           ]")
    m.vEmiNOxTot          = Var  (                                 m.sYear,                within = NonNegativeReals, doc = "Total NOx emissions produced yearly                                                          [MtNOx           ]")
    m.vEmiNOxCapExc       = Var  (                                 m.sYear,                within = NonNegativeReals, doc = "Excess of NOx emissions regarding cap 2050 onwards (slack variable)                          [MtNOx           ]")
                    
    #SOx Emission variables                               
    m.vEmiSOxCE           = Var  (      m.sCE,                     m.sYear,                within = NonNegativeReals, doc = "SOx emissions produced in CE processes                                                       [ktSOx           ]")
    m.vEmiSOxCEPri        = Var  (m.sQCEPriIN,                     m.sYear,                within = NonNegativeReals, doc = "SOx emissions produced in Primary CE processes                                               [ tSOx           ]")
    m.vEmiSOxCESec        = Var  (m.sQCESecIN,                     m.sYear,                within = NonNegativeReals, doc = "SOx emissions produced in Secondary CE processes                                             [ tSOx           ]")
    m.vEmiSOxCESto        = Var  (m.sQCEStoIN,                     m.sYear,                within = NonNegativeReals, doc = "SOx emissions produced in Storage CE processes                                               [ tSOx           ]")
    m.vEmiSOxSTTE         = Var  (            m.sQTESTES,          m.sYear,                within = NonNegativeReals, doc = "SOx emissions produced in ST due to TE consumption                                           [ tSOx           ]")
    m.vEmiSOxSTPro        = Var  (                  m.sQSTOUT,     m.sYear,                within = NonNegativeReals, doc = "SOx emissions produced in ST due to activity processes                                       [ tSOx           ]")
    m.vEmiSOxST           = Var  (                  m.sQSTOUT,     m.sYear,                within = NonNegativeReals, doc = "SOx emissions produced in ST                                                                 [ktSOx           ]")
    m.vEmiSOxESNS         = Var  (                                 m.sYear,                within = NonNegativeReals, doc = "SOx emissions related to ESNS                                                                [ktSOx           ]")
    m.vEmiSOxTot          = Var  (                                 m.sYear,                within = NonNegativeReals, doc = "Total SOx emissions produced yearly                                                          [MtSOx           ]")
    m.vEmiSOxCapExc       = Var  (                                 m.sYear,                within = NonNegativeReals, doc = "Excess of SOx emissions regarding cap 2050 onwards (slack variable)                          [MtSOx           ]")
                    
    #PM25 Emission variables                               
    m.vEmiPM25CE          = Var  (      m.sCE,                     m.sYear,                within = NonNegativeReals, doc = "PM25 emissions produced in CE processes                                                      [ktPM25          ]")
    m.vEmiPM25CEPri       = Var  (m.sQCEPriIN,                     m.sYear,                within = NonNegativeReals, doc = "PM25 emissions produced in Primary CE processes                                              [ tPM25          ]")
    m.vEmiPM25CESec       = Var  (m.sQCESecIN,                     m.sYear,                within = NonNegativeReals, doc = "PM25 emissions produced in Secondary CE processes                                            [ tPM25          ]")
    m.vEmiPM25CESto       = Var  (m.sQCEStoIN,                     m.sYear,                within = NonNegativeReals, doc = "PM25 emissions produced in Storage CE processes                                              [ tPM25          ]")
    m.vEmiPM25STTE        = Var  (            m.sQTESTES,          m.sYear,                within = NonNegativeReals, doc = "PM25 emissions produced in ST due to TE consumption                                          [ tPM25          ]")
    m.vEmiPM25STPro       = Var  (                  m.sQSTOUT,     m.sYear,                within = NonNegativeReals, doc = "PM25 emissions produced in ST due to activity processes                                      [ tPM25          ]")
    m.vEmiPM25ST          = Var  (                  m.sQSTOUT,     m.sYear,                within = NonNegativeReals, doc = "PM25 emissions produced in ST                                                                [ktPM25          ]")
    m.vEmiPM25ESNS        = Var  (                                 m.sYear,                within = NonNegativeReals, doc = "PM25 emissions related to ESNS                                                               [ktPM25          ]")
    m.vEmiPM25CapExc      = Var  (                                 m.sYear,                within = NonNegativeReals, doc = "Excess of PM25 emissions regarding cap 2050 onwards (slack variable)                         [MtPM25          ]")
    m.vEmiPM25Tot         = Var  (                                 m.sYear,                within = NonNegativeReals, doc = "Total PM25 emissions produced yearly                                                         [MtPM25          ]")
    
    
    #CO2 sectorial emission slack variables  
    m.vEmiCO2CapTraExc    = Var  (                                 m.sYear,                within = NonNegativeReals, doc = "Excess of CO2 emissions regarding Carbon Cap in Transport sector            (slack variable) [MtCO2           ]")
    m.vEmiCO2CapEleExc    = Var  (                                 m.sYear,                within = NonNegativeReals, doc = "Excess of CO2 emissions regarding Carbon Cap in Electricity generation      (slack variable) [MtCO2           ]")
    m.vEmiCO2CapIndTEExc  = Var  (                                 m.sYear,                within = NonNegativeReals, doc = "Excess of CO2 emissions regarding Carbon Cap in Industrial sector (energy)  (slack variable) [MtCO2           ]")
    m.vEmiCO2CapIndProExc = Var  (                                 m.sYear,                within = NonNegativeReals, doc = "Excess of CO2 emissions regarding Carbon Cap in Industrial sector (process) (slack variable) [MtCO2           ]")
    m.vEmiCO2CapOthExc    = Var  (                                 m.sYear,                within = NonNegativeReals, doc = "Excess of CO2 emissions regarding Carbon Cap in Residential&Service sector  (slack variable) [MtCO2           ]")
    m.vEmiCO2CapRefExc    = Var  (                                 m.sYear,                within = NonNegativeReals, doc = "Excess of CO2 emissions regarding Carbon Cap in Refinery sector             (slack variable) [MtCO2           ]")
    
    
    
    d = dict()
    
    # ### **Equations**
    # #### Objective function
    ######################################################################################################################################################################
    ######################################################################################################################################################################
    # Objective function begin --------------------------------------------------------------------------------------------------------------------------------------------------
    
    def EQ_FObj            (m               ):
        return  (m.vSysCost)
    d['EQ_FObj']             = Objective (sense = minimize,       rule = EQ_FObj,            doc = 'Total system cost minimization objective function')

    # Where vSysCost is the total system cost [G€]
    def EQ_SysCost           (m        ):
        return m.vSysCost ==        (sum(m.vTotalCost      [sYear] for       sYear  in       m.sYear)  
                            +        sum(m.vPenalCost      [sYear] for       sYear  in       m.sYear)
                            +        sum(m.vBMCost     [sBM,sYear] for (sBM, sYear) in m.sBM*m.sYear)
                            +        sum(m.vDMCost     [sDM,sYear] for (sDM, sYear) in m.sDM*m.sYear)
                            +            m.pEmiCO2BudgetRestr * m.vEmiCO2BudgetExc
                            )
    #G€
    d['EQ_SysCost']              = Constraint(                 rule = EQ_SysCost,             doc = 'Total System Cost [G€]')

        # Where vTotalCost is the annual total cost [G€]
    def EQ_TotalCost         (m, sYear        ):
        return m.vTotalCost[sYear] ==  (1e-3*m.vOpCost[sYear]) + sum(m.vInvCostCE[sCE,sYear] for sCE in m.sCE) + sum(m.vInvCostSTRes[sST_Res,sYear] for sST_Res in m.sST_Res) + sum(m.vInvCostSTTra[sST_Tra,sYear] for sST_Tra in m.sST_Tra) + sum(m.vInvCostSTInd[sST_Ind,sYear] for sST_Ind in m.sST_Ind) + sum(m.vInvCostSTOth[sST_Oth,sYear] for sST_Oth in m.sST_Oth)
    #G€
    d['EQ_TotalCost']            = Constraint(m.sYear,         rule = EQ_TotalCost,           doc = 'Annual Total Cost = Total Investment Cost + Total Operation Cost [G€]')

    # vInvCostCE is the annual total CE investment cost [G€]
    def EQ_InvCostCE         (m, sCE, sYear        ):
         return m.vInvCostCE[sCE,sYear] == (1/((1+m.pDisRate)**(m.pYrGap*(m.sYear.ord(sYear)-1)))) * (
                                            m.pCECapex[sCE,sYear] * m.vCENewCap     [sCE,sYear] 
                                          + m.pCEDecom[sCE,sYear] * m.vCEDecCap     [sCE,sYear] 
                                          + m.pCEReact[sCE,sYear] * m.vCEDeltaActCap[sCE,sYear]
                                           ) *1e-3
    #G€
    d['EQ_InvCostCE']            = Constraint(m.sCE, m.sYear,  rule = EQ_InvCostCE,           doc = 'Annual Total CE Investment Cost [G€]')

    # Where vInvCostSTTra is the annual total ST Tra Investment Cost [G€]
    def EQ_InvCostSTTra      (m, sST_Tra, sYear        ):
        return m.vInvCostSTTra[sST_Tra,sYear] == (1/((1+m.pDisRate)**(m.pYrGap*(m.sYear.ord(sYear)-1)))) * (
                                            m.pSTCapexTra[sST_Tra,sYear] *          m.vSTNewCapTra     [sST_Tra,     sYear]
                                            + m.pSTDecomTra[sST_Tra,sYear] *    sum(m.vSTDecCapTra     [sST_Tra,sVin,sYear] for sVin in m.sVin if (sVin,sYear) in m.sVinYear)
                                            ) *1e-3
    #G€
    d['EQ_InvCostSTTra']            = Constraint(m.sST_Tra, m.sYear,  rule = EQ_InvCostSTTra,           doc = 'Annual Total ST Tra Investment Cost [G€]')

    # Where vInvCostSTInd is the annual total ST Ind Investment Cost [G€]
    def EQ_InvCostSTInd      (m, sST_Ind, sYear        ):
        return m.vInvCostSTInd[sST_Ind,sYear] == (1/((1+m.pDisRate)**(m.pYrGap*(m.sYear.ord(sYear)-1)))) * (
                                              m.pSTCapexInd[sST_Ind,sYear] *        m.vSTNewCapInd     [sST_Ind,     sYear]
                                            + m.pSTDecomInd[sST_Ind,sYear] *    sum(m.vSTDecCapInd     [sST_Ind,sVin,sYear] for sVin in m.sVin if (sVin,sYear) in m.sVinYear)
                                            ) *1e-3
    #G€
    d['EQ_InvCostSTInd']            = Constraint(m.sST_Ind, m.sYear,  rule = EQ_InvCostSTInd,           doc = 'Annual Total ST Ind Investment Cost [G€]')

    # Where vInvCostSTOth is the annual total ST Oth Investment Cost [G€]
    def EQ_InvCostSTOth      (m, sST_Oth, sYear        ):
        return m.vInvCostSTOth[sST_Oth,sYear] == (1/((1+m.pDisRate)**(m.pYrGap*(m.sYear.ord(sYear)-1)))) * (
                                              m.pSTCapexOth[sST_Oth,sYear] *        m.vSTNewCapOth     [sST_Oth,     sYear]
                                            + m.pSTDecomOth[sST_Oth,sYear] *    sum(m.vSTDecCapOth     [sST_Oth,sVin,sYear] for sVin in m.sVin if (sVin,sYear) in m.sVinYear)
                                            ) *1e-3
    #G€
    d['EQ_InvCostSTOth']            = Constraint(m.sST_Oth, m.sYear,  rule = EQ_InvCostSTOth,           doc = 'Annual Total ST Oth Investment Cost [G€]')

    # Where vInvCostSTRes is the annual total ST Res Investment Cost [G€]
    def EQ_InvCostSTRes      (m, sST_Res,sYear        ):
         return m.vInvCostSTRes[sST_Res,sYear] == (1/((1+m.pDisRate)**(m.pYrGap*(m.sYear.ord(sYear)-1)))) * (
                                            m.pSTCapexRes[sST_Res,sYear] *  sum(m.vSTNewCapRes     [sST_Res, sES_Res, sSD_Res, sMD_Res, sYear] for (sES_Res, sSD_Res, sMD_Res) in m.sES_Res*m.sSD_Res*m.sMD_Res if (sST_Res,sES_Res,sSD_Res,sMD_Res,sYear) in m.sQSTESSDMD_Res)
                                          + m.pSTDecomRes[sST_Res,sYear] *  sum(sum(m.vSTDecCapRes     [sST_Res, sES_Res,sMD_Res,sSD_Res,sVin,sYear]        for (sVin) in m.sVin if (sVin,sYear) in m.sVinYear) for (sES_Res,sMD_Res,sSD_Res) in m.sES_Res*m.sMD_Res*m.sSD_Res if (sST_Res,sES_Res,sMD_Res,sSD_Res) in m.sQSTESSDMD_Res)
                                           ) *1e-3
    #G€
    d['EQ_InvCostSTRes']            = Constraint(m.sST_Res, m.sYear,  rule = EQ_InvCostSTRes,           doc = 'Annual Total ST Res Investment Cost [G€]')

    # Where vOpCost is the annual total operation cost [G€]
    # vOpCost is the annual total operation cost [M€]
    def EQ_OpCost         (m, sYear        ):
        return m.vOpCost[sYear] ==   m.pYrGap * (1/((1+m.pDisRate)**(m.pYrGap*(m.sYear.ord(sYear)-1)))) *(
                                    sum(m.pPECost [sPE,sYear] *    (m.vQPEImp  [sPE,             sYear,sSeason,sDay,sHour] + m.vQPEDom[sPE,sYear,sSeason,sDay,sHour]) for (sPE,sSeason,sDay,sHour) in m.sPEYearTime)                                                                                                                      
                            + 1e3 * sum(m.pCEFixom[sCE]       *     m.vCEActCap[sCE,             sYear                    ] for sCE                                          in m.sCE) 
                            + 1e3 * sum(m.pRMCost [sRM,sYear] *     m.vQSTInRM [sRM,sST,sES,sVin,sYear,sSeason,sDay,sHour]  for (_,sRM,sST,sES,sVin,sSeason,sDay,sHour)      in m.sQSTInRM_indexed[sYear])
                            + 1e-3* sum(m.pSTFixomTra[sST_Tra      ] *     m.vSTTotCapTra[    sST_Tra,    sVin,sYear                    ]  for (_,sST_Tra,sVin)                                 in m.sQSTVinTra_indexed[sYear])
                            + 1e-3* sum(m.pSTFixomOth[sST_Oth      ] *     m.vSTTotCapOth[    sST_Oth,    sVin,sYear                    ]  for (_,sST_Oth,sVin)                                 in m.sQSTVinOth_indexed[sYear])
                            + 1e-3* sum(m.pSTFixomInd[sST_Ind      ] *     m.vSTTotCapInd[    sST_Ind,    sVin,sYear                    ]  for (_,sST_Ind,sVin)                                 in m.sQSTVinInd_indexed[sYear])
                            + 1e-3* sum(m.pSTFixomRes[sST_Res      ] *     m.vSTTotCapRes[    sST_Res,    sVin,sYear                    ]  for (_,sST_Res,sVin)                                 in m.sQSTVinRes_indexed[sYear])
                            + 1e-3* sum(m.pSTVaromTra[sST_Tra,sES_Tra] *    (m.vQSTOut_Tra  [    sST_Tra,sES_Tra,sVin,sYear,sSeason,sDay,sHour]) for (_,sST_Tra,sES_Tra,sVin,sSeason,sDay,sHour)          in m.sQSTOUTTra_VinTime_indexed[sYear]) 
                            + 1e-3* sum(m.pSTVaromOth[sST_Oth,sES_Oth] *    (m.vQSTOut_Oth  [    sST_Oth,sES_Oth,sVin,sYear,sSeason,sDay,sHour]) for (_,sST_Oth,sES_Oth,sVin,sSeason,sDay,sHour)          in m.sQSTOUTOth_VinTime_indexed[sYear])
                            + 1e-3* sum(m.pSTVaromInd[sST_Ind,sES_Ind] *    (m.vQSTOut_Ind  [    sST_Ind,sES_Ind,sVin,sYear,sSeason,sDay,sHour]) for (_,sST_Ind,sES_Ind,sVin,sSeason,sDay,sHour)          in m.sQSTOUTInd_VinTime_indexed[sYear])
                            + 1e-3* sum(m.pSTVaromRes[sST_Res,sES_Res] *    (m.vQSTOut_Res  [    sST_Res,sES_Res,sSD_Res,sMD_Res,sVin,sYear,sSeason,sDay,sHour]) for (_,sST_Res,sES_Res,sSD_Res,sMD_Res,sVin,sSeason,sDay,sHour) in m.sQSTOUTRes_VinTime_indexed[sYear])
                           #+ 1e3*      m.pESNSCost           * sum(m.vQESNS   [sST,sES,         sYear,sSeason,sDay,sHour]  for (_,sST,sES,sSeason,sDay,sHour)               in m.sQSTOUT_Time_indexed[sYear])
                            +           m.vOpVarom[sYear]  
                            ) * 1e-3
    #M€
    d['EQ_OpCost']               = Constraint(m.sYear,         rule = EQ_OpCost,              doc = 'Annual Total Operation Cost [M€]')

    # vOpVarom is the annual total operation variable cost [k€]
    def EQ_OpVarom         (m, sYear        ):
        return m.vOpVarom[sYear] ==  (
    
                                   + sum(m.pCEVarom[sCE,sTE] * (m.vQCEPriOUT[sCE,sTE,sYear,sSeason,sDay,sHour]) for (_,sCE,sTE,sSeason,sDay,sHour) in m.sQCEPriOUT_Time_indexed[sYear])
                                   + sum(m.pCEVarom[sCE,sTE] * (m.vQCESecOUT[sCE,sTE,sYear,sSeason,sDay,sHour]) for (_,sCE,sTE,sSeason,sDay,sHour) in m.sQCESecOUT_Time_indexed[sYear])
                                   + sum(m.pCEVarom[sCE,sTE] * (m.vQCEStoOUT[sCE,sTE,sYear,sSeason,sDay,sHour]) for (_,sCE,sTE,sSeason,sDay,sHour) in m.sQCEStoOUT_Time_indexed[sYear])
                                                                         
                                    )
    #k€
    d['EQ_OpVarom']              = Constraint(m.sYear,         rule = EQ_OpVarom,             doc = 'Annual Total Varom Cost [k€]')

    # vPenalCost is the penalization cost [G€]
    def EQ_PenalCost           (m, sYear ):
        return m.vPenalCost [sYear] ==  m.pYrGap * (1/((1+m.pDisRate)**(m.pYrGap*(m.sYear.ord(sYear)-1)))) * 1e-2* m.pESNSCost * ( 
                             + (1-m.pEmiCO2CapSectRestr) * (1 - m.pEmiCO2BudgetRestr) *      m.vEmiCO2CapExc   [sYear]
                             +    m.pEmiCO2CapSectRestr  * (1 - m.pEmiCO2BudgetRestr) * sum((m.vEmiCO2CapTraExc[sYear] + m.vEmiCO2CapEleExc[sYear] + m.vEmiCO2CapIndTEExc[sYear] + m.vEmiCO2CapIndProExc[sYear] + m.vEmiCO2CapOthExc[sYear] + m.vEmiCO2CapRefExc[sYear]) for sYear in m.sYear)
                             +                                                          sum((m.vEmiNOxCapExc   [sYear] + m.vEmiSOxCapExc   [sYear] + m.vEmiPM25CapExc    [sYear]                                                                                       ) for sYear in m.sYear)
                            )
    #G€
    d['EQ_PenalCost']            = Constraint(m.sYear,         rule = EQ_PenalCost,           doc = 'Penalization Cost [G€]')

    # vBMCost is the annual BM cost [G€]
    def EQ_BMCost         (m, sBM,sYear        ):
        return m.vBMCost[sBM,sYear] == (1/((1+m.pDisRate)**(m.pYrGap*(m.sYear.ord(sYear)-1)))) * (
                                        sum(m.pBMCost[sBM,sYear] * m.vBMTra[sST_Tra,sES_Tra,sSD_Tra,sBM,sYear] for (sST_Tra,sES_Tra,sSD_Tra) in m.sQSTESSD_Tra if sBM in m.sBM_Tra) 
                                      + sum(m.pBMCost[sBM,sYear] * m.vBMOth[sES_Res,sSD_Res,sMD_Res,sBM,sYear] for (sES_Res,sSD_Res,sMD_Res) in m.sQESSDMD_Res if sBM in m.sBM_Res)
                                      )
    #G€
    d['EQ_BMCost']               = Constraint(m.sBM,m.sYear,   rule = EQ_BMCost,              doc = 'Annual BM Cost [G€]')

    # vDMCost is the annual DM cost [G€]
    def EQ_DMCost         (m, sDM,sYear        ):
        return m.vDMCost[sDM,sYear] == (1/((1+m.pDisRate)**(m.pYrGap*(m.sYear.ord(sYear)-1)))) * (
                                        sum(m.pDMCost          [sDM,             sYear] *  m.vDMTra   [sSD_Tra,sMD_Tra,sDM,sYear] for (sSD_Tra,sMD_Tra) in m.sQSDMD_Tra if sDM in m.sDM_Tra) 
                                      + sum(m.pDMCost          [sDM,             sYear] * (m.vDMRes_HE[        sMD_Res,sDM,sYear] 
                                      -    (m.vDMRes_HE[sMD_Res,sDM,m.sYear.prev(sYear)] if not sYear==m.sYear.first() else 0))   for  sMD_Res          in m.sMD_Res    if sDM in m.sDM_Res)
                                      )
    #G€
    d['EQ_DMCost']               = Constraint(m.sDM,m.sYear,   rule = EQ_DMCost,              doc = 'Annual DM Cost [G€]')

    # Objective function end  --------------------------------------------------------------------------------------------------------------------------------------------------

    # Primary energy (PE)-related constraints begin --------------------------------------------------------------------------------------------------------------------------------------------------
    # vQPEDom is the annual domestic PE production [GWh]
    def EQ_PEDomCap         (m, sPE, sYear, sSeason, sDay, sHour        ):
        return m.pPEDomCap [sPE] * m.pNumHours * m.pTimeSlice [sSeason,sDay,sHour] >= m.vQPEDom   [sPE,sYear,sSeason,sDay,sHour]
    #GWh
    d['EQ_PEDomCap']            = Constraint(m.sPE,m.sTime,         rule = EQ_PEDomCap,           doc = 'PE domestic production capacity [GWh]')

    # vQPEImp is the annual imported PE [GWh]
    def EQ_PEImpCap         (m, sPE, sYear, sSeason, sDay, sHour        ):
        return m.pPEImpCap [sPE] * m.pNumHours * m.pTimeSlice [sSeason,sDay,sHour] >= m.vQPEImp [sPE,sYear,sSeason,sDay,sHour]
    #GWh
    d['EQ_PEImpCap']            = Constraint(m.sPE,m.sTime,         rule = EQ_PEImpCap,           doc = 'PE importation capacity [GWh]') 

    # PE energy balance
    def EQ_PEBalance         (m, sPE, sYear, sSeason, sDay, sHour        ):
        return m.vQPEDom[sPE,sYear,sSeason,sDay,sHour] + m.vQPEImp[sPE,sYear,sSeason,sDay,sHour] == sum(m.vQCEPriIN[sPE,sCE,sYear,sSeason,sDay,sHour] for (_,sCE) in m.sQCEPriIN_indexed[sPE])
    #GWh
    d['EQ_PEBalance']           = Constraint(m.sPE,m.sTime,         rule = EQ_PEBalance,          doc = 'PE energy balance [GWh]')
    # Primary energy (PE)-related constraints end --------------------------------------------------------------------------------------------------------------------------------------------------

    # Primary Conversion Energy (CE_Pri)-related contraints begin --------------------------------------------------------------------------------------------------------------------------------------------------
    # Balance for Primary CE techs (using PE commodities)
    def EQ_CEPriBalance         (m, sCEPri, sYear, sSeason, sDay, sHour        ):
        return (sum(((m.vQCEPriIN [sPE,sCEPri,sYear,sSeason,sDay,sHour] if (sPE,sCEPri) in m.sQCEPriIN  else 0) * (m.pCEPriEff[sPE, sCEPri] if (sPE,sCEPri) in m.sQCEPriIN else 0)) for sPE in m.sPE) 
            ==  sum(( m.vQCEPriOUT[sCEPri,sTE,sYear,sSeason,sDay,sHour] if (sCEPri,sTE) in m.sQCEPriOUT else 0)                                                                     for sTE in m.sTE))
    #GWh
    d['EQ_CEPriBalance']            = Constraint(m.sCEPri,m.sTime,         rule = EQ_CEPriBalance,           doc = 'Balance for Primary CE techs (using PE commodities) [GWh]')

    # Lower bound for Primary CE output shares
    def EQ_CEPriOutShareMin         (m, sCEPri,sTE,sYear,sSeason,sDay,sHour        ):
        return m.vQCEPriOUT [sCEPri,sTE,sYear,sSeason,sDay,sHour] >=  m.pCEOutShareMin [sCEPri,sTE] * sum(m.vQCEPriOUT [sCEPri,sTE,sYear,sSeason,sDay,sHour] for (_,sTE) in m.sQCEPriOUT_CE_indexed[sCEPri])
    #GWh
    d['EQ_CEPriOutShareMin']        = Constraint(m.sQCEPriOUT,m.sTime,     rule = EQ_CEPriOutShareMin,       doc = 'Minimum CE output shares restriction [GWh]')

    # Upper bound for Primary CE output shares
    def EQ_CEPriOutShareMax         (m, sCEPri,sTE,sYear,sSeason,sDay,sHour        ):
        return m.pCEOutShareMax [sCEPri,sTE] * sum(m.vQCEPriOUT [sCEPri,sTE,sYear,sSeason,sDay,sHour] for (_,sTE) in m.sQCEPriOUT_CE_indexed[sCEPri]) >= m.vQCEPriOUT [sCEPri,sTE,sYear,sSeason,sDay,sHour]
    #GWh
    d['EQ_CEPriOutShareMax']        = Constraint(m.sQCEPriOUT,m.sTime,     rule = EQ_CEPriOutShareMax,       doc = 'Maximum CE output shares restriction [GWh]')

    # Primary Conversion Energy (CE_Pri)-related contraints end --------------------------------------------------------------------------------------------------------------------------------------------------

    # Secondary Conversion Energy (CE_Sec)-related constraints begin --------------------------------------------------------------------------------------------------------------------------------------------------

    # Balance for Secondary CE techs (using TE commodities)
    def EQ_CESecBalance         (m, sCESec,sYear,sSeason,sDay,sHour        ): 
        return (sum(((m.vQCESecIN [sTE,sCESec,sYear,sSeason,sDay,sHour] if (sTE,sCESec) in m.sQCESecIN  else 0) * (m.pCESecEff[sTE, sCESec] if (sTE, sCESec) in m.sQCESecIN else 0)) for sTE in m.sTE) 
           ==   sum(( m.vQCESecOUT[sCESec,sTE,sYear,sSeason,sDay,sHour] if (sCESec,sTE) in m.sQCESecOUT else 0)                                                                      for sTE in m.sTE))
    #GWh
    d['EQ_CESecBalance']            = Constraint(m.sCESec,m.sTime,         rule = EQ_CESecBalance,           doc = 'Balance for CE techs using TE commodities [GWh]')

    # Lower bound for Secondary CE output shares
    def EQ_CESecOutShareMin         (m, sCESec,sTE,sYear,sSeason,sDay,sHour        ):
        return m.vQCESecOUT [sCESec,sTE,sYear,sSeason,sDay,sHour] >= m.pCEOutShareMin [sCESec,sTE] * sum(m.vQCESecOUT [sCESec,sTE,sYear,sSeason,sDay,sHour] for (_,sTE) in m.sQCESecOUT_CE_indexed[sCESec])
    #GWh
    d['EQ_CESecOutShareMin']        = Constraint(m.sQCESecOUT,m.sTime,     rule = EQ_CESecOutShareMin,       doc = 'Minimum CE output shares restriction [GWh]')

    # Upper bound for Secondary CE output shares
    def EQ_CESecOutShareMax         (m, sCESec,sTE,sYear,sSeason,sDay,sHour        ):
        return m.pCEOutShareMax[sCESec,sTE] * sum(m.vQCESecOUT [sCESec,sTE,sYear,sSeason,sDay,sHour] for (_,sTE) in m.sQCESecOUT_CE_indexed[sCESec]) >= m.vQCESecOUT [sCESec,sTE,sYear,sSeason,sDay,sHour]
    #GWh
    d['EQ_CESecOutShareMax']        = Constraint(m.sQCESecOUT,m.sTime,     rule = EQ_CESecOutShareMax,       doc = 'Maximum CE output shares restriction [GWh]')

    # Secondary Conversion Energy (CE_Sec)-related constraints end --------------------------------------------------------------------------------------------------------------------------------------------------

    # Storage-related constraints begin --------------------------------------------------------------------------------------------------------------------------------------------------

    # Balance for storage seasonal representative-day
    def EQ_CEStoBalance         (m, sCESto,sYear,sSeason        ):
        return (sum((m.vQCEStoIN [sTE,sCESto,sYear,sSeason,sDay,sHour] * (m.pCEStoEff[sTE, sCESto] if (sTE, sCESto) in m.sQCEStoIN else 0)) for (sTE,sDay,sHour) in m.sTE*m.sDay*m.sHour if ((sTE,sCESto) in m.sQCEStoIN ))
             == sum( m.vQCEStoOUT[sCESto,sTE,sYear,sSeason,sDay,sHour]                                                                      for (sTE,sDay,sHour) in m.sTE*m.sDay*m.sHour if  (sCESto,sTE) in m.sQCEStoOUT))
    #GWh (Seasonal balance)
    d['EQ_CEStoBalance']          = Constraint(m.sCESto,m.sYear,m.sSeason,  rule = EQ_CEStoBalance,         doc = 'Balance for storage seasonal representative-day [GWh]')

    # Storage level calculation
    def EQ_CEStoLevel         (m, sCESto,sYear,sSeason,sDay,sHour        ):
        return           m.vCEStoLevel [    sCESto,    sYear,sSeason,  sDay,             sHour] ==(
                  +     (m.vCEStoLevel [    sCESto,    sYear,sSeason,  sDay,           m.sHour.prev(sHour)] if not sHour==m.sHour.first()                               else 0)  # if         h>00 --> level(d     , h-1   )
                  +     (m.vCEStoLevel [    sCESto,    sYear,sSeason,m.sDay.prev(sDay),m.sHour.last()     ] if    (sHour==m.sHour.first() and not sDay==m.sDay.first()) else 0)  # if d>0 and h=00 --> level(d-1   , h.l
                  +     (m.vCEStoLevel [    sCESto,    sYear,sSeason,m.sDay.last()    ,m.sHour.last()     ] if    (sHour==m.sHour.first() and     sDay==m.sDay.first()) else 0)  # if d=0 and h=00 --> level(d.last, h.last)              
                  + sum((m.vQCEStoIN   [sTE,sCESto,    sYear,sSeason,  sDay,             sHour            ] * (m.pCEStoEff[sTE, sCESto] if (sTE, sCESto) in m.sQCEStoIN else 0)) for sTE in m.sTE if ((sTE,sCESto) in m.sQCEStoIN))
                  - sum(m.vQCEStoOUT   [    sCESto,sTE,sYear,sSeason,  sDay,             sHour            ]                                                                      for sTE in m.sTE if ((sCESto,sTE) in m.sQCEStoOUT)))
    #GWh
    d['EQ_CEStoLevel']            = Constraint(m.sCESto,m.sTime,            rule = EQ_CEStoLevel,           doc = 'Storage level calculation [GWh]')

    # Minimum Storage output shares
    def EQ_CEStoOutShareMin         (m, sCESto,sTE,sYear,sSeason,sDay,sHour        ):
        return m.vQCEStoOUT  [sCESto,sTE,sYear,sSeason,sDay,sHour]                    >=  m.pCEOutShareMin [sCESto,sTE] * sum(m.vQCEStoOUT  [sCESto,sTE,sYear,sSeason,sDay,sHour] for (_,sTE) in m.sQCEStoOUT_CE_indexed[sCESto])
    #GWh
    d['EQ_CEStoOutShareMin']      = Constraint(m.sQCEStoOUT,m.sTime,        rule = EQ_CEStoOutShareMin,     doc = 'Minimum Storage output shares [GWh]')

    # Maximum Storage output shares
    def EQ_CEStoOutShareMax         (m, sCESto,sTE,sYear,sSeason,sDay,sHour        ):
        return m.pCEOutShareMax [sCESto,sTE] * sum(m.vQCEStoOUT  [sCESto,sTE,sYear,sSeason,sDay,sHour] for (_,sTE) in m.sQCEStoOUT_CE_indexed[sCESto]) >= m.vQCEStoOUT [sCESto,sTE,sYear,sSeason,sDay,sHour]
    #GWh
    d['EQ_CEStoOutShareMax']      = Constraint(m.sQCEStoOUT,m.sTime,        rule = EQ_CEStoOutShareMax,     doc = 'Maximum Storage output shares [GWh]')

    # Storage maximum level restriction
    def EQ_CEStoMaxSto         (m, sCESto,sYear,sSeason,sDay,sHour        ):
        return m.pCEStoCap [sCESto] >= m.vCEStoLevel [sCESto,sYear,sSeason,sDay,sHour]
    #GWh
    d['EQ_CEStoMaxSto']           = Constraint(m.sCESto,m.sTime,            rule = EQ_CEStoMaxSto,          doc = 'Storage maximum level restriction [GWh]')
    
    # Storage-related constraints end --------------------------------------------------------------------------------------------------------------------------------------------------
    
    # Transformed Energy (TE)-related constraints begin --------------------------------------------------------------------------------------------------------------------------------------------------

    # Balance for TE
    def EQ_TEBalance             (m, sTE,sYear,sSeason,sDay,sHour  ):
              
        return  (quicksum(m.vQCEPriOUT [sCE,sTE,         sYear,sSeason,sDay,sHour] for (_,sCE)            in m.sQCEPriOUT_indexed[sTE]       ) 
               + quicksum(m.vQCESecOUT [sCE,sTE,         sYear,sSeason,sDay,sHour] for (_,sCE)            in m.sQCESecOUT_indexed[sTE]       ) 
               + quicksum(m.vQCEStoOUT [sCE,sTE,         sYear,sSeason,sDay,sHour] for (_,sCE)            in m.sQCEStoOUT_indexed[sTE]       ) 
               - quicksum(m.vQCESecIN  [sTE,sCE,         sYear,sSeason,sDay,sHour] for (_,sCE)            in m.sQCESecIN_indexed [sTE]       ) 
               - quicksum(m.vQCEStoIN  [sTE,sCE,         sYear,sSeason,sDay,sHour] for (_,sCE)            in m.sQCEStoIN_indexed [sTE]       )     
               -          m.vQTELoss   [sTE,             sYear,sSeason,sDay,sHour] 
              >= quicksum(m.vQSTTraInTE   [sTE,sST,sES,sVin,sYear,sSeason,sDay,sHour] for (_,_,sST,sES,sVin) in m.sSTTraESVin_indexed  [sTE, sYear])
               + quicksum(m.vQSTOthInTE   [sTE,sST,sES,sVin,sYear,sSeason,sDay,sHour] for (_,_,sST,sES,sVin) in m.sSTOthESVin_indexed  [sTE, sYear])
               + quicksum(m.vQSTIndInTE   [sTE,sST,sES,sVin,sYear,sSeason,sDay,sHour] for (_,_,sST,sES,sVin) in m.sSTIndESVin_indexed  [sTE, sYear])
               + quicksum(m.vQSTResInTE   [sTE,sST,sES,sVin,sYear,sSeason,sDay,sHour] for (_,_,sST,sES,sVin) in m.sSTResESVin_indexed  [sTE, sYear]))
    #GWh
    d['EQ_TEBalance']            = Constraint(m.sTE,m.sTime,         rule = EQ_TEBalance,           doc = 'Balance for TE [GWh]')
   
    # TE losses for transportation processes
    def EQ_TELoss         (m, sTE,sYear,sSeason,sDay,sHour        ):
        return  (m.vQTELoss [sTE,sYear,sSeason,sDay,sHour]  ==  m.pTELoss[sTE] * (
                                                            sum(m.vQCEPriOUT [sCE,sTE,sYear,sSeason,sDay,sHour] for (_,sCE) in m.sQCEPriOUT_indexed[sTE]) 
                                                          + sum(m.vQCESecOUT [sCE,sTE,sYear,sSeason,sDay,sHour] for (_,sCE) in m.sQCESecOUT_indexed[sTE]) 
                                                          + sum(m.vQCEStoOUT [sCE,sTE,sYear,sSeason,sDay,sHour] for (_,sCE) in m.sQCEStoOUT_indexed[sTE])))
    #GWh
    d['EQ_TELoss']               = Constraint(m.sTE,m.sTime,         rule = EQ_TELoss,              doc = 'TE losses for transportation processes [GWh]')

    # Transformed Energy (TE)-related constraints end --------------------------------------------------------------------------------------------------------------------------------------------------

    # Supply Technologies (ST)-related constraints begin --------------------------------------------------------------------------------------------------------------------------------------------------
    # ST Transport consumption of TE
    def EQ_STBalanceTE_Tra         (m, sST_Tra,sES_Tra,sVin,sYear,sSeason,sDay,sHour        ):
        return sum((m.vQSTTraInTE [sTE,sST_Tra,sES_Tra,sVin,sYear,sSeason,sDay,sHour] / m.pSTEffTE[sST_Tra,sES_Tra,sTE,sVin]) for (_,_,sTE) in m.sQTESTES_STES_indexed[sST_Tra,sES_Tra]) == m.vQSTOut_Tra [sST_Tra,sES_Tra,sVin,sYear,sSeason,sDay,sHour]
    #ES units
    d['EQ_STBalanceTE_Tra']            = Constraint(m.sQSTOUT_Tra,m.sVinTime,         rule = EQ_STBalanceTE_Tra,           doc = 'Balance for ST Tra consumption of TE [ES units]')

    # ST Other consumption of TE
    def EQ_STBalanceTE_Oth         (m, sST_Oth,sES_Oth,sVin,sYear,sSeason,sDay,sHour        ):
        return sum((m.vQSTOthInTE [sTE,sST_Oth,sES_Oth,sVin,sYear,sSeason,sDay,sHour] / m.pSTEffTE[sST_Oth,sES_Oth,sTE,sVin]) for (_,_,sTE) in m.sQTESTES_STES_indexed[sST_Oth,sES_Oth]) == m.vQSTOut_Oth [sST_Oth,sES_Oth,sVin,sYear,sSeason,sDay,sHour]
    #ES units
    d['EQ_STBalanceTE_Oth']            = Constraint(m.sQSTOUT_Oth,m.sVinTime,         rule = EQ_STBalanceTE_Oth,           doc = 'Balance for ST Oth consumption of TE [ES units]')

    # ST Industry consumption of TE
    def EQ_STBalanceTE_Ind     (m, sTE, sST_Ind,sES_Ind,sVin,sYear,sSeason,sDay,sHour        ):
        return  m.vQSTIndInTE [sTE,sST_Ind,sES_Ind,sVin,sYear,sSeason,sDay,sHour] / m.pSTEffTE[sST_Ind,sES_Ind,sTE,sVin] == m.vQSTOut_Ind [sST_Ind,sES_Ind,sVin,sYear,sSeason,sDay,sHour]
    #ES units
    d['EQ_STBalanceTE_Ind']            = Constraint(m.sQTESTES_Ind,m.sVinTime,        rule = EQ_STBalanceTE_Ind,           doc = 'Balance for ST Ind consumption of TE [ES units]')

    # ST Residential consumption of TE
    def EQ_STBalanceTE_Res     (m,sTE, sST_Res,sES_Res,sVin,sYear,sSeason,sDay,sHour        ):
        return  sum(m.vQSTResInTE [sTE,sST_Res,sES_Res,sVin,sYear,sSeason,sDay,sHour] / m.pSTEffTE[sST_Res,sES_Res,sTE,sVin] for (_,_,sTE) in m.sQTESTES_STES_indexed[sST_Res,sES_Res]) == m.vQSTOut_Res [sST_Res,sES_Res,sVin,sYear,sSeason,sDay,sHour]
    #ES units
    d['EQ_STBalanceTE_Res']            = Constraint(m.sQSTOUT_Res,m.sVinTime,        rule = EQ_STBalanceTE_Res,           doc = 'Balance for ST Res consumption of TE [ES units]')

    # Minimum ST output shares restriction
    def EQ_STOutShareMin         (m, sST,sES,sVin,sYear,sSeason,sDay,sHour        ):
        return m.vQSTOut [sST,sES,sVin,sYear,sSeason,sDay,sHour] >= m.pSTOutShareMin [sST,sES] * sum(m.vQSTOut [sST,sES,sVin,sYear,sSeason,sDay,sHour] for (_,sES) in m.sQSTOUT_indexed[sST])
    #GWh
    d['EQ_STOutShareMin']              = Constraint(m.sQSTOUT,m.sVinTime,             rule = EQ_STOutShareMin,             doc = 'Minimum ST output shares restriction [ES units]')

    # Maximum ST output shares restriction
    def EQ_STOutShareMax         (m, sST,sES,sVin,sYear,sSeason,sDay,sHour        ):
        return m.pSTOutShareMax[sST,sES] * sum(m.vQSTOut [sST,sES,sVin,sYear,sSeason,sDay,sHour] for (_,sES) in m.sQSTOUT_indexed[sST]) >= m.vQSTOut [sST,sES,sVin,sYear,sSeason,sDay,sHour]
    #GWh
    d['EQ_STOutShareMax']              = Constraint(m.sQSTOUT,m.sVinTime,             rule = EQ_STOutShareMax,             doc = 'Maximum ES output shares restriction [ES units]')
    # Supply Technologies (ST)-related constraints end --------------------------------------------------------------------------------------------------------------------------------------------------

    # Transport modal shift constraints
    #MINIMUM MODAL SHARE
    
    
    def EQ_MinMS_Car         (m, sSD_Tra_Car,sYear       ):
        if sYear>m.sYear.first():
            return  1e4*(sum((m.vQES_Tra[sST_Tra_Car,sES_Tra,sYear] * m.pAFTra[sST_Tra_Car,sES_Tra,sSD_Tra_Car]) for (_,sES_Tra,sST_Tra_Car) in m.sQSTOUT_AFTraCar_indexed[sSD_Tra_Car])/sum(m.pDC[sSD_Tra_Car,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Car])) >= 1e4*(sum((m.vQES_Tra[sST_Tra_Car,sES_Tra,m.sYear.prev(sYear)] * m.pAFTra[sST_Tra_Car,sES_Tra,sSD_Tra_Car]) for (_,sES_Tra,sST_Tra_Car) in m.sQSTOUT_AFTraCar_indexed[sSD_Tra_Car])/sum(m.pDC[sSD_Tra_Car,sMD_Tra] * m.pMD[sMD_Tra,m.sYear.prev(sYear)] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Car])) - 1e4*m.pMSMax
        else:
            return  1e4*(sum((m.vQES_Tra[sST_Tra_Car,sES_Tra,sYear] * m.pAFTra[sST_Tra_Car,sES_Tra,sSD_Tra_Car]) for (_,sES_Tra,sST_Tra_Car) in m.sQSTOUT_AFTraCar_indexed[sSD_Tra_Car])/sum(m.pDC[sSD_Tra_Car,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Car])) >= 1e4*m.pSTTra_MS['Car',sSD_Tra_Car]
    #GWh
    d['EQ_MinMS_Car']            = Constraint(m.sSD_Tra_Car, m.sYear,        rule = EQ_MinMS_Car,           doc = 'Minimum ST output shares restriction [ES units]')
    
    def EQ_MinMS_Bus         (m, sSD_Tra_Bus,sYear       ):
        if sYear>m.sYear.first():
            return  1e4*(sum((m.vQES_Tra[sST_Tra_Bus,sES_Tra,sYear] * m.pAFTra[sST_Tra_Bus,sES_Tra,sSD_Tra_Bus]) for (_,sES_Tra,sST_Tra_Bus) in m.sQSTOUT_AFTraBus_indexed[sSD_Tra_Bus])/sum(m.pDC[sSD_Tra_Bus,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Bus])) >= 1e4*( (sum((m.vQES_Tra[sST_Tra_Bus,sES_Tra,m.sYear.prev(sYear)] * m.pAFTra[sST_Tra_Bus,sES_Tra,sSD_Tra_Bus]) for (_,sES_Tra,sST_Tra_Bus) in m.sQSTOUT_AFTraBus_indexed[sSD_Tra_Bus])/sum(m.pDC[sSD_Tra_Bus,sMD_Tra] * m.pMD[sMD_Tra,m.sYear.prev(sYear)] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Bus]))) - 1e4*m.pMSMax
        else:
            return  1e4*(sum((m.vQES_Tra[sST_Tra_Bus,sES_Tra,sYear] * m.pAFTra[sST_Tra_Bus,sES_Tra,sSD_Tra_Bus]) for (_,sES_Tra,sST_Tra_Bus) in m.sQSTOUT_AFTraBus_indexed[sSD_Tra_Bus])/sum(m.pDC[sSD_Tra_Bus,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Bus])) >= 1e4*m.pSTTra_MS['Bus',sSD_Tra_Bus]
    #GWh
    d['EQ_MinMS_Bus']            = Constraint(m.sSD_Tra_Bus, m.sYear,        rule = EQ_MinMS_Bus,           doc = 'Minimum ST output shares restriction [ES units]')
    
    def EQ_MinMS_Moped         (m, sSD_Tra_Moped,sYear       ):
        if sYear>m.sYear.first():
            return  1e4*(sum((m.vQES_Tra[sST_Tra_Moped,sES_Tra,sYear] * m.pAFTra[sST_Tra_Moped,sES_Tra,sSD_Tra_Moped]) for (_,sES_Tra,sST_Tra_Moped) in m.sQSTOUT_AFTraMoped_indexed[sSD_Tra_Moped])/sum(m.pDC[sSD_Tra_Moped,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Moped])) >= 1e4*((sum((m.vQES_Tra[sST_Tra_Moped,sES_Tra,m.sYear.prev(sYear)] * m.pAFTra[sST_Tra_Moped,sES_Tra,sSD_Tra_Moped]) for (_,sES_Tra,sST_Tra_Moped) in m.sQSTOUT_AFTraMoped_indexed[sSD_Tra_Moped])/sum(m.pDC[sSD_Tra_Moped,sMD_Tra] * m.pMD[sMD_Tra,m.sYear.prev(sYear)] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Moped]))) - 1e4*m.pMSMax
        else:
            return  1e4*(sum((m.vQES_Tra[sST_Tra_Moped,sES_Tra,sYear] * m.pAFTra[sST_Tra_Moped,sES_Tra,sSD_Tra_Moped]) for (_,sES_Tra,sST_Tra_Moped) in m.sQSTOUT_AFTraMoped_indexed[sSD_Tra_Moped])/sum(m.pDC[sSD_Tra_Moped,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Moped])) >= 1e4*m.pSTTra_MS['Moped',sSD_Tra_Moped]
    #GWh
    d['EQ_MinMS_Moped']          = Constraint(m.sSD_Tra_Moped, m.sYear,      rule = EQ_MinMS_Moped,         doc = 'Minimum ST output shares restriction [ES units]')
    
    def EQ_MinMS_IntRail         (m, sSD_Tra_IntRail,sYear       ):
        if sYear>m.sYear.first():
            return  1e4*(sum((m.vQES_Tra[sST_Tra_IntRail,sES_Tra,sYear] * m.pAFTra[sST_Tra_IntRail,sES_Tra,sSD_Tra_IntRail]) for (_,sES_Tra,sST_Tra_IntRail) in m.sQSTOUT_AFTraIntRail_indexed[sSD_Tra_IntRail])/sum(m.pDC[sSD_Tra_IntRail,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_IntRail])) >= 1e4*( (sum((m.vQES_Tra[sST_Tra_IntRail,sES_Tra,m.sYear.prev(sYear)] * m.pAFTra[sST_Tra_IntRail,sES_Tra,sSD_Tra_IntRail]) for (_,sES_Tra,sST_Tra_IntRail) in m.sQSTOUT_AFTraIntRail_indexed[sSD_Tra_IntRail])/sum(m.pDC[sSD_Tra_IntRail,sMD_Tra] * m.pMD[sMD_Tra,m.sYear.prev(sYear)] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_IntRail]))) - 1e4*m.pMSMax
        else:
            return  1e4*(sum((m.vQES_Tra[sST_Tra_IntRail,sES_Tra,sYear] * m.pAFTra[sST_Tra_IntRail,sES_Tra,sSD_Tra_IntRail]) for (_,sES_Tra,sST_Tra_IntRail) in m.sQSTOUT_AFTraIntRail_indexed[sSD_Tra_IntRail])/sum(m.pDC[sSD_Tra_IntRail,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_IntRail])) >= 1e4*m.pSTTra_MS['IntRail',sSD_Tra_IntRail]
    #GWh
    d['EQ_MinMS_IntRail']        = Constraint(m.sSD_Tra_IntRail, m.sYear,    rule = EQ_MinMS_IntRail,       doc = 'Minimum ST output shares restriction [ES units]')
    
    def EQ_MinMS_UrbanRail         (m, sSD_Tra_UrbanRail,sYear       ):
        if sYear>m.sYear.first():
            return  1e4*(sum((m.vQES_Tra[sST_Tra_UrbanRail,sES_Tra,sYear] * m.pAFTra[sST_Tra_UrbanRail,sES_Tra,sSD_Tra_UrbanRail]) for (_,sES_Tra,sST_Tra_UrbanRail) in m.sQSTOUT_AFTraUrbRail_indexed[sSD_Tra_UrbanRail])/sum(m.pDC[sSD_Tra_UrbanRail,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_UrbanRail])) >= 1e4*( (sum((m.vQES_Tra[sST_Tra_UrbanRail,sES_Tra,m.sYear.prev(sYear)] * m.pAFTra[sST_Tra_UrbanRail,sES_Tra,sSD_Tra_UrbanRail]) for (_,sES_Tra,sST_Tra_UrbanRail) in m.sQSTOUT_AFTraUrbRail_indexed[sSD_Tra_UrbanRail])/sum(m.pDC[sSD_Tra_UrbanRail,sMD_Tra] * m.pMD[sMD_Tra,m.sYear.prev(sYear)] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_UrbanRail]))) - 1e4*m.pMSMax
        else:
            return  1e4*(sum((m.vQES_Tra[sST_Tra_UrbanRail,sES_Tra,sYear] * m.pAFTra[sST_Tra_UrbanRail,sES_Tra,sSD_Tra_UrbanRail]) for (_,sES_Tra,sST_Tra_UrbanRail) in m.sQSTOUT_AFTraUrbRail_indexed[sSD_Tra_UrbanRail])/sum(m.pDC[sSD_Tra_UrbanRail,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_UrbanRail])) >= 1e4*m.pSTTra_MS['UrbanRail',sSD_Tra_UrbanRail]
    #GWh
    d['EQ_MinMS_UrbanRail']      = Constraint(m.sSD_Tra_UrbanRail, m.sYear,  rule = EQ_MinMS_UrbanRail,     doc = 'Minimum ST output shares restriction [ES units]')
    
    def EQ_MinMS_Air         (m, sSD_Tra_Air,sYear       ):
        if sYear>m.sYear.first():
            return  1e4*(sum((m.vQES_Tra[sST_Tra_Air,sES_Tra,sYear] * m.pAFTra[sST_Tra_Air,sES_Tra,sSD_Tra_Air]) for (_,sES_Tra,sST_Tra_Air) in m.sQSTOUT_AFTraAir_indexed[sSD_Tra_Air])/sum(m.pDC[sSD_Tra_Air,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Air])) >= 1e4*( (sum((m.vQES_Tra[sST_Tra_Air,sES_Tra,m.sYear.prev(sYear)] * m.pAFTra[sST_Tra_Air,sES_Tra,sSD_Tra_Air]) for (_,sES_Tra,sST_Tra_Air) in m.sQSTOUT_AFTraAir_indexed[sSD_Tra_Air])/sum(m.pDC[sSD_Tra_Air,sMD_Tra] * m.pMD[sMD_Tra,m.sYear.prev(sYear)] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Air]))) - 1e4*m.pMSMax
        else:
            return  1e4*(sum((m.vQES_Tra[sST_Tra_Air,sES_Tra,sYear] * m.pAFTra[sST_Tra_Air,sES_Tra,sSD_Tra_Air]) for (_,sES_Tra,sST_Tra_Air) in m.sQSTOUT_AFTraAir_indexed[sSD_Tra_Air])/sum(m.pDC[sSD_Tra_Air,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Air])) >= 1e4*m.pSTTra_MS['Air',sSD_Tra_Air]
    #GWh
    d['EQ_MinMS_Air']            = Constraint(m.sSD_Tra_Air, m.sYear,        rule = EQ_MinMS_Air,           doc = 'Minimum ST output shares restriction [ES units]')
    
    def EQ_MinMS_Sea         (m, sSD_Tra_Sea,sYear       ):
        if sYear>m.sYear.first():
            return  1e4*(sum((m.vQES_Tra[sST_Tra_Sea,sES_Tra,sYear] * m.pAFTra[sST_Tra_Sea,sES_Tra,sSD_Tra_Sea]) for (_,sES_Tra,sST_Tra_Sea) in m.sQSTOUT_AFTraSea_indexed[sSD_Tra_Sea])/sum(m.pDC[sSD_Tra_Sea,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Sea])) >= 1e4*( (sum((m.vQES_Tra[sST_Tra_Sea,sES_Tra,m.sYear.prev(sYear)] * m.pAFTra[sST_Tra_Sea,sES_Tra,sSD_Tra_Sea]) for (_,sES_Tra,sST_Tra_Sea) in m.sQSTOUT_AFTraSea_indexed[sSD_Tra_Sea])/sum(m.pDC[sSD_Tra_Sea,sMD_Tra] * m.pMD[sMD_Tra,m.sYear.prev(sYear)] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Sea]))) - 1e4*m.pMSMax
        else:
            return  1e4*(sum((m.vQES_Tra[sST_Tra_Sea,sES_Tra,sYear] * m.pAFTra[sST_Tra_Sea,sES_Tra,sSD_Tra_Sea]) for (_,sES_Tra,sST_Tra_Sea) in m.sQSTOUT_AFTraSea_indexed[sSD_Tra_Sea])/sum(m.pDC[sSD_Tra_Sea,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Sea])) >= 1e4*m.pSTTra_MS['Sea',sSD_Tra_Sea]
    #GWh
    d['EQ_MinMS_Sea']            = Constraint(m.sSD_Tra_Sea, m.sYear,        rule = EQ_MinMS_Sea,           doc = 'Minimum ST output shares restriction [ES units]')
    
    
    #MAXIMUM MODAL SHARE
    
    def EQ_MaxMS_Car         (m, sSD_Tra_Car,sYear       ):
        if sYear>m.sYear.first():
            return  1e4*(sum((m.vQES_Tra[sST_Tra_Car,sES_Tra,sYear] * m.pAFTra[sST_Tra_Car,sES_Tra,sSD_Tra_Car]) for (_,sES_Tra,sST_Tra_Car) in m.sQSTOUT_AFTraCar_indexed[sSD_Tra_Car])/sum(m.pDC[sSD_Tra_Car,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Car])) <= 1e4*(sum((m.vQES_Tra[sST_Tra_Car,sES_Tra,m.sYear.prev(sYear)] * m.pAFTra[sST_Tra_Car,sES_Tra,sSD_Tra_Car]) for (_,sES_Tra,sST_Tra_Car) in m.sQSTOUT_AFTraCar_indexed[sSD_Tra_Car])/sum(m.pDC[sSD_Tra_Car,sMD_Tra] * m.pMD[sMD_Tra,m.sYear.prev(sYear)] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Car])) + 1e4*m.pMSMax
        else:
            return  1e4*(sum((m.vQES_Tra[sST_Tra_Car,sES_Tra,sYear] * m.pAFTra[sST_Tra_Car,sES_Tra,sSD_Tra_Car]) for (_,sES_Tra,sST_Tra_Car) in m.sQSTOUT_AFTraCar_indexed[sSD_Tra_Car])/sum(m.pDC[sSD_Tra_Car,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Car])) <= 1e4*m.pSTTra_MS['Car',sSD_Tra_Car]
    #GWh
    d['EQ_MaxMS_Car']            = Constraint(m.sSD_Tra_Car, m.sYear,        rule = EQ_MaxMS_Car,           doc = 'Minimum ST output shares restriction [ES units]')
    
    def EQ_MaxMS_Bus         (m, sSD_Tra_Bus,sYear       ):
        if sYear>m.sYear.first():
            return  1e4*(sum((m.vQES_Tra[sST_Tra_Bus,sES_Tra,sYear] * m.pAFTra[sST_Tra_Bus,sES_Tra,sSD_Tra_Bus]) for (_,sES_Tra,sST_Tra_Bus) in m.sQSTOUT_AFTraBus_indexed[sSD_Tra_Bus])/sum(m.pDC[sSD_Tra_Bus,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Bus])) <= 1e4*( (sum((m.vQES_Tra[sST_Tra_Bus,sES_Tra,m.sYear.prev(sYear)] * m.pAFTra[sST_Tra_Bus,sES_Tra,sSD_Tra_Bus]) for (_,sES_Tra,sST_Tra_Bus) in m.sQSTOUT_AFTraBus_indexed[sSD_Tra_Bus])/sum(m.pDC[sSD_Tra_Bus,sMD_Tra] * m.pMD[sMD_Tra,m.sYear.prev(sYear)] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Bus]))) + 1e4*m.pMSMax
        else:
            return  1e4*(sum((m.vQES_Tra[sST_Tra_Bus,sES_Tra,sYear] * m.pAFTra[sST_Tra_Bus,sES_Tra,sSD_Tra_Bus]) for (_,sES_Tra,sST_Tra_Bus) in m.sQSTOUT_AFTraBus_indexed[sSD_Tra_Bus])/sum(m.pDC[sSD_Tra_Bus,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Bus])) <= 1e4*m.pSTTra_MS['Bus',sSD_Tra_Bus]
    #GWh
    d['EQ_MaxMS_Bus']            = Constraint(m.sSD_Tra_Bus, m.sYear,        rule = EQ_MaxMS_Bus,           doc = 'Minimum ST output shares restriction [ES units]')
    
    def EQ_MaxMS_Moped         (m, sSD_Tra_Moped,sYear       ):
        if sYear>m.sYear.first():
            return  1e4*(sum((m.vQES_Tra[sST_Tra_Moped,sES_Tra,sYear] * m.pAFTra[sST_Tra_Moped,sES_Tra,sSD_Tra_Moped]) for (_,sES_Tra,sST_Tra_Moped) in m.sQSTOUT_AFTraMoped_indexed[sSD_Tra_Moped])/sum(m.pDC[sSD_Tra_Moped,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Moped])) <= 1e4*((sum((m.vQES_Tra[sST_Tra_Moped,sES_Tra,m.sYear.prev(sYear)] * m.pAFTra[sST_Tra_Moped,sES_Tra,sSD_Tra_Moped]) for (_,sES_Tra,sST_Tra_Moped) in m.sQSTOUT_AFTraMoped_indexed[sSD_Tra_Moped])/sum(m.pDC[sSD_Tra_Moped,sMD_Tra] * m.pMD[sMD_Tra,m.sYear.prev(sYear)] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Moped]))) + 1e4*m.pMSMax
        else:
            return  1e4*(sum((m.vQES_Tra[sST_Tra_Moped,sES_Tra,sYear] * m.pAFTra[sST_Tra_Moped,sES_Tra,sSD_Tra_Moped]) for (_,sES_Tra,sST_Tra_Moped) in m.sQSTOUT_AFTraMoped_indexed[sSD_Tra_Moped])/sum(m.pDC[sSD_Tra_Moped,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Moped])) <= 1e4*m.pSTTra_MS['Moped',sSD_Tra_Moped]
    #GWh
    d['EQ_MaxMS_Moped']          = Constraint(m.sSD_Tra_Moped, m.sYear,      rule = EQ_MaxMS_Moped,         doc = 'Minimum ST output shares restriction [ES units]')
    
    def EQ_MaxMS_IntRail         (m, sSD_Tra_IntRail,sYear       ):
        if sYear>m.sYear.first():
            return  1e4*(sum((m.vQES_Tra[sST_Tra_IntRail,sES_Tra,sYear] * m.pAFTra[sST_Tra_IntRail,sES_Tra,sSD_Tra_IntRail]) for (_,sES_Tra,sST_Tra_IntRail) in m.sQSTOUT_AFTraIntRail_indexed[sSD_Tra_IntRail])/sum(m.pDC[sSD_Tra_IntRail,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_IntRail])) <= 1e4*( (sum((m.vQES_Tra[sST_Tra_IntRail,sES_Tra,m.sYear.prev(sYear)] * m.pAFTra[sST_Tra_IntRail,sES_Tra,sSD_Tra_IntRail]) for (_,sES_Tra,sST_Tra_IntRail) in m.sQSTOUT_AFTraIntRail_indexed[sSD_Tra_IntRail])/sum(m.pDC[sSD_Tra_IntRail,sMD_Tra] * m.pMD[sMD_Tra,m.sYear.prev(sYear)] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_IntRail]))) + 1e4*m.pMSMax
        else:
            return  1e4*(sum((m.vQES_Tra[sST_Tra_IntRail,sES_Tra,sYear] * m.pAFTra[sST_Tra_IntRail,sES_Tra,sSD_Tra_IntRail]) for (_,sES_Tra,sST_Tra_IntRail) in m.sQSTOUT_AFTraIntRail_indexed[sSD_Tra_IntRail])/sum(m.pDC[sSD_Tra_IntRail,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_IntRail])) <= 1e4*m.pSTTra_MS['IntRail',sSD_Tra_IntRail]
    #GWh
    d['EQ_MaxMS_IntRail']        = Constraint(m.sSD_Tra_IntRail, m.sYear,    rule = EQ_MaxMS_IntRail,       doc = 'Minimum ST output shares restriction [ES units]')
    
    def EQ_MaxMS_UrbanRail         (m, sSD_Tra_UrbanRail,sYear       ):
        if sYear>m.sYear.first():
            return  1e4*(sum((m.vQES_Tra[sST_Tra_UrbanRail,sES_Tra,sYear] * m.pAFTra[sST_Tra_UrbanRail,sES_Tra,sSD_Tra_UrbanRail]) for (_,sES_Tra,sST_Tra_UrbanRail) in m.sQSTOUT_AFTraUrbRail_indexed[sSD_Tra_UrbanRail])/sum(m.pDC[sSD_Tra_UrbanRail,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_UrbanRail])) <= 1e4*( (sum((m.vQES_Tra[sST_Tra_UrbanRail,sES_Tra,m.sYear.prev(sYear)] * m.pAFTra[sST_Tra_UrbanRail,sES_Tra,sSD_Tra_UrbanRail]) for (_,sES_Tra,sST_Tra_UrbanRail) in m.sQSTOUT_AFTraUrbRail_indexed[sSD_Tra_UrbanRail])/sum(m.pDC[sSD_Tra_UrbanRail,sMD_Tra] * m.pMD[sMD_Tra,m.sYear.prev(sYear)] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_UrbanRail]))) + 1e4*m.pMSMax
        else:
            return  1e4*(sum((m.vQES_Tra[sST_Tra_UrbanRail,sES_Tra,sYear] * m.pAFTra[sST_Tra_UrbanRail,sES_Tra,sSD_Tra_UrbanRail]) for (_,sES_Tra,sST_Tra_UrbanRail) in m.sQSTOUT_AFTraUrbRail_indexed[sSD_Tra_UrbanRail])/sum(m.pDC[sSD_Tra_UrbanRail,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_UrbanRail])) <= 1e4*m.pSTTra_MS['UrbanRail',sSD_Tra_UrbanRail]
    #GWh
    d['EQ_MaxMS_UrbanRail']      = Constraint(m.sSD_Tra_UrbanRail, m.sYear,  rule = EQ_MaxMS_UrbanRail,     doc = 'Minimum ST output shares restriction [ES units]')
    
    def EQ_MaxMS_Air         (m, sSD_Tra_Air,sYear       ):
        if sYear>m.sYear.first():
            return  1e4*(sum((m.vQES_Tra[sST_Tra_Air,sES_Tra,sYear] * m.pAFTra[sST_Tra_Air,sES_Tra,sSD_Tra_Air]) for (_,sES_Tra,sST_Tra_Air) in m.sQSTOUT_AFTraAir_indexed[sSD_Tra_Air])/sum(m.pDC[sSD_Tra_Air,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Air])) <= 1e4*( (sum((m.vQES_Tra[sST_Tra_Air,sES_Tra,m.sYear.prev(sYear)] * m.pAFTra[sST_Tra_Air,sES_Tra,sSD_Tra_Air]) for (_,sES_Tra,sST_Tra_Air) in m.sQSTOUT_AFTraAir_indexed[sSD_Tra_Air])/sum(m.pDC[sSD_Tra_Air,sMD_Tra] * m.pMD[sMD_Tra,m.sYear.prev(sYear)] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Air]))) + 1e4*m.pMSMax
        else:
            return  1e4*(sum((m.vQES_Tra[sST_Tra_Air,sES_Tra,sYear] * m.pAFTra[sST_Tra_Air,sES_Tra,sSD_Tra_Air]) for (_,sES_Tra,sST_Tra_Air) in m.sQSTOUT_AFTraAir_indexed[sSD_Tra_Air])/sum(m.pDC[sSD_Tra_Air,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Air])) <= 1e4*m.pSTTra_MS['Air',sSD_Tra_Air]
    #GWh
    d['EQ_MaxMS_Air']            = Constraint(m.sSD_Tra_Air, m.sYear,        rule = EQ_MaxMS_Air,           doc = 'Minimum ST output shares restriction [ES units]')
    
    def EQ_MaxMS_Sea         (m, sSD_Tra_Sea,sYear       ):
        if sYear>m.sYear.first():
            return  1e4*(sum((m.vQES_Tra[sST_Tra_Sea,sES_Tra,sYear] * m.pAFTra[sST_Tra_Sea,sES_Tra,sSD_Tra_Sea]) for (_,sES_Tra,sST_Tra_Sea) in m.sQSTOUT_AFTraSea_indexed[sSD_Tra_Sea])/sum(m.pDC[sSD_Tra_Sea,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Sea])) <= 1e4*( (sum((m.vQES_Tra[sST_Tra_Sea,sES_Tra,m.sYear.prev(sYear)] * m.pAFTra[sST_Tra_Sea,sES_Tra,sSD_Tra_Sea]) for (_,sES_Tra,sST_Tra_Sea) in m.sQSTOUT_AFTraSea_indexed[sSD_Tra_Sea])/sum(m.pDC[sSD_Tra_Sea,sMD_Tra] * m.pMD[sMD_Tra,m.sYear.prev(sYear)] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Sea]))) + 1e4*m.pMSMax
        else:
            return  1e4*(sum((m.vQES_Tra[sST_Tra_Sea,sES_Tra,sYear] * m.pAFTra[sST_Tra_Sea,sES_Tra,sSD_Tra_Sea]) for (_,sES_Tra,sST_Tra_Sea) in m.sQSTOUT_AFTraSea_indexed[sSD_Tra_Sea])/sum(m.pDC[sSD_Tra_Sea,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra_Sea])) <= 1e4*m.pSTTra_MS['Sea',sSD_Tra_Sea]
    #GWh
    d['EQ_MaxMS_Sea']            = Constraint(m.sSD_Tra_Sea, m.sYear,        rule = EQ_MaxMS_Sea,           doc = 'Minimum ST output shares restriction [ES units]')
    
    
    # Technological choice shares
    def EQ_TC_Car         (m, sST_Tra_Car,sYear       ):
        if sYear>m.sYear.first():
            return  m.vSTNewCapTra [sST_Tra_Car,sYear] <= sum(m.vSTTotCapTra [sST_Tra_Car,sVin,m.sYear.prev(sYear)] for sVin in m.sVin if (sVin,m.sYear.prev(sYear)) in m.sVinYear) + m.pTCMax * sum(m.vSTTotCapTra [sST_Tra_Car,sVin,m.sYear.prev(sYear)] for (sST_Tra_Car,sVin) in m.sST_Tra_Car*m.sVin if (sVin,m.sYear.prev(sYear)) in m.sVinYear)
        else:
            return  m.vSTNewCapTra [sST_Tra_Car,sYear] <= sum(m.pSTInsCap [sST_Tra_Car,sVin]                     for sVin in m.sVin if (sVin,             sYear)  in m.sVinYear) + m.pTCMax * sum(m.pSTInsCap [sST_Tra_Car,sVin]                     for (sST_Tra_Car,sVin) in m.sST_Tra_Car*m.sVin if (sVin,             sYear)  in m.sVinYear)
    #GWh
    d['EQ_TC_Car']                  = Constraint(m.sST_Tra_Car, m.sYear,        rule = EQ_TC_Car,           doc = '[ST units]')
    
    
    def EQ_TC_Moped         (m, sST_Tra_Moped,sYear       ):
        if sYear>m.sYear.first():
            return  m.vSTNewCapTra [sST_Tra_Moped,sYear] <= sum(m.vSTTotCapTra [sST_Tra_Moped,sVin,m.sYear.prev(sYear)] for sVin in m.sVin if (sVin,m.sYear.prev(sYear)) in m.sVinYear) + m.pTCMax * sum(m.vSTTotCapTra [sST_Tra_Moped,sVin,m.sYear.prev(sYear)] for (sST_Tra_Moped,sVin) in m.sST_Tra_Moped*m.sVin if (sVin,m.sYear.prev(sYear)) in m.sVinYear)
        else:
            return  m.vSTNewCapTra [sST_Tra_Moped,sYear] <= sum(m.pSTInsCap [sST_Tra_Moped,sVin]                     for sVin in m.sVin if (sVin,             sYear)  in m.sVinYear) + m.pTCMax * sum(m.pSTInsCap [sST_Tra_Moped,sVin]                     for (sST_Tra_Moped,sVin) in m.sST_Tra_Moped*m.sVin if (sVin,             sYear)  in m.sVinYear)
    #GWh
    d['EQ_TC_Moped']                = Constraint(m.sST_Tra_Moped, m.sYear,      rule = EQ_TC_Moped,         doc = '[ST units]')
    
    
    def EQ_TC_RoadFreight         (m, sST_Tra_RoadFreight,sYear       ):
        if sYear>m.sYear.first():
            return  m.vSTNewCapTra [sST_Tra_RoadFreight,sYear] <= sum(m.vSTTotCapTra [sST_Tra_RoadFreight,sVin,m.sYear.prev(sYear)] for sVin in m.sVin if (sVin,m.sYear.prev(sYear)) in m.sVinYear) + m.pTCMax * sum(m.vSTTotCapTra [sST_Tra_RoadFreight,sVin,m.sYear.prev(sYear)] for (sST_Tra_RoadFreight,sVin) in m.sST_Tra_RoadFreight*m.sVin if (sVin,m.sYear.prev(sYear)) in m.sVinYear)
        else:
            return  m.vSTNewCapTra [sST_Tra_RoadFreight,sYear] <= sum(m.pSTInsCap [sST_Tra_RoadFreight,sVin]                     for sVin in m.sVin if (sVin,             sYear)  in m.sVinYear) + m.pTCMax * sum(m.pSTInsCap [sST_Tra_RoadFreight,sVin]                     for (sST_Tra_RoadFreight,sVin) in m.sST_Tra_RoadFreight*m.sVin if (sVin,             sYear)  in m.sVinYear)
    #GWh
    d['EQ_TC_RoadFreight']          = Constraint(m.sST_Tra_RoadFreight, m.sYear,rule = EQ_TC_RoadFreight,   doc = '[ST units]')
    
    
    def EQ_TC_Bus         (m, sST_Tra_Bus,sYear       ):
        if sYear>m.sYear.first():
            return  m.vSTNewCapTra [sST_Tra_Bus,sYear] <= sum(m.vSTTotCapTra [sST_Tra_Bus,sVin,m.sYear.prev(sYear)] for sVin in m.sVin if (sVin,m.sYear.prev(sYear)) in m.sVinYear) + m.pTCMax * sum(m.vSTTotCapTra [sST_Tra_Bus,sVin,m.sYear.prev(sYear)] for (sST_Tra_Bus,sVin) in m.sST_Tra_Bus*m.sVin if (sVin,m.sYear.prev(sYear)) in m.sVinYear)
        else:
            return  m.vSTNewCapTra [sST_Tra_Bus,sYear] <= sum(m.pSTInsCap [sST_Tra_Bus,sVin]                     for sVin in m.sVin if (sVin,             sYear)  in m.sVinYear) + m.pTCMax * sum(m.pSTInsCap [sST_Tra_Bus,sVin]                     for (sST_Tra_Bus,sVin) in m.sST_Tra_Bus*m.sVin if (sVin,             sYear)  in m.sVinYear)
    #GWh
    d['EQ_TC_Bus']                  = Constraint(m.sST_Tra_Bus, m.sYear,        rule = EQ_TC_Bus,           doc = '[ST units]')
    
    
    def EQ_TC_UrbanRail         (m, sST_Tra_UrbanRail,sYear       ):
        if sYear>m.sYear.first():
            return  m.vSTNewCapTra [sST_Tra_UrbanRail,sYear] <= sum(m.vSTTotCapTra [sST_Tra_UrbanRail,sVin,m.sYear.prev(sYear)] for sVin in m.sVin if (sVin,m.sYear.prev(sYear)) in m.sVinYear) + m.pTCMax * sum(m.vSTTotCapTra [sST_Tra_UrbanRail,sVin,m.sYear.prev(sYear)] for (sST_Tra_UrbanRail,sVin) in m.sST_Tra_UrbanRail*m.sVin if (sVin,m.sYear.prev(sYear)) in m.sVinYear)
        else:
            return  m.vSTNewCapTra [sST_Tra_UrbanRail,sYear] <= sum(m.pSTInsCap [sST_Tra_UrbanRail,sVin]                     for sVin in m.sVin if (sVin,             sYear)  in m.sVinYear) + m.pTCMax * sum(m.pSTInsCap [sST_Tra_UrbanRail,sVin]                     for (sST_Tra_UrbanRail,sVin) in m.sST_Tra_UrbanRail*m.sVin if (sVin,             sYear)  in m.sVinYear)
    #GWh
    d['EQ_TC_UrbanRail']            = Constraint(m.sST_Tra_UrbanRail, m.sYear,  rule = EQ_TC_UrbanRail,     doc = '[ST units]')
    
    
    def EQ_TC_IntRail         (m, sST_Tra_IntRail,sYear       ):
        if sYear>m.sYear.first():
            return  m.vSTNewCapTra [sST_Tra_IntRail,sYear] <= sum(m.vSTTotCapTra [sST_Tra_IntRail,sVin,m.sYear.prev(sYear)] for sVin in m.sVin if (sVin,m.sYear.prev(sYear)) in m.sVinYear) + m.pTCMax * sum(m.vSTTotCapTra [sST_Tra_IntRail,sVin,m.sYear.prev(sYear)] for (sST_Tra_IntRail,sVin) in m.sST_Tra_IntRail*m.sVin if (sVin,m.sYear.prev(sYear)) in m.sVinYear)
        else:
            return  m.vSTNewCapTra [sST_Tra_IntRail,sYear] <= sum(m.pSTInsCap [sST_Tra_IntRail,sVin]                     for sVin in m.sVin if (sVin,             sYear)  in m.sVinYear) + m.pTCMax * sum(m.pSTInsCap [sST_Tra_IntRail,sVin]                     for (sST_Tra_IntRail,sVin) in m.sST_Tra_IntRail*m.sVin if (sVin,             sYear)  in m.sVinYear)
    #GWh
    d['EQ_TC_IntRail']              = Constraint(m.sST_Tra_IntRail, m.sYear,    rule = EQ_TC_IntRail,       doc = '[ST units]')
    
    
    def EQ_TC_Air         (m, sST_Tra_Air,sYear       ):
        if sYear>m.sYear.first():
            return  m.vSTNewCapTra [sST_Tra_Air,sYear] <= sum(m.vSTTotCapTra [sST_Tra_Air,sVin,m.sYear.prev(sYear)] for sVin in m.sVin if (sVin,m.sYear.prev(sYear)) in m.sVinYear) + m.pTCMax * sum(m.vSTTotCapTra [sST_Tra_Air,sVin,m.sYear.prev(sYear)] for (sST_Tra_Air,sVin) in m.sST_Tra_Air*m.sVin if (sVin,m.sYear.prev(sYear)) in m.sVinYear)
        else:
            return  m.vSTNewCapTra [sST_Tra_Air,sYear] <= sum(m.pSTInsCap [sST_Tra_Air,sVin]                     for sVin in m.sVin if (sVin,             sYear)  in m.sVinYear) + m.pTCMax * sum(m.pSTInsCap [sST_Tra_Air,sVin]                     for (sST_Tra_Air,sVin) in m.sST_Tra_Air*m.sVin if (sVin,             sYear)  in m.sVinYear)
    #GWh
    d['EQ_TC_Air']                  = Constraint(m.sST_Tra_Air, m.sYear,        rule = EQ_TC_Air,           doc = '[ST units]')
    
    
    def EQ_TC_Sea         (m, sST_Tra_Sea,sYear       ):
        if sYear>m.sYear.first():
            return  m.vSTNewCapTra [sST_Tra_Sea,sYear] <= sum(m.vSTTotCapTra [sST_Tra_Sea,sVin,m.sYear.prev(sYear)] for sVin in m.sVin if (sVin,m.sYear.prev(sYear)) in m.sVinYear) + m.pTCMax * sum(m.vSTTotCapTra [sST_Tra_Sea,sVin,m.sYear.prev(sYear)] for (sST_Tra_Sea,sVin) in m.sST_Tra_Sea*m.sVin if (sVin,m.sYear.prev(sYear)) in m.sVinYear)
        else:
            return  m.vSTNewCapTra [sST_Tra_Sea,sYear] <= sum(m.pSTInsCap [sST_Tra_Sea,sVin]                     for sVin in m.sVin if (sVin,             sYear)  in m.sVinYear) + m.pTCMax * sum(m.pSTInsCap [sST_Tra_Sea,sVin]                     for (sST_Tra_Sea,sVin) in m.sST_Tra_Sea*m.sVin if (sVin,             sYear)  in m.sVinYear)
    #GWh
    d['EQ_TC_Sea']                  = Constraint(m.sST_Tra_Sea, m.sYear,        rule = EQ_TC_Sea,           doc = '[ST units]')

    def EQ_TC_Res         (m, sST_Res,sES_Res,sYear       ):
        if sYear>m.sYear.first():
            return  m.vSTNewCapRes [sST_Res,sYear] <= sum(m.vSTTotCapRes [sST_Res,sVin,m.sYear.prev(sYear)] for sVin in m.sVin if (sST_Res,sES_Res) in m.sQSTOUT_Res if (sVin,m.sYear.prev(sYear)) in m.sVinYear) + m.pTCMax * sum(m.vSTTotCapRes [sST_Res,sVin,m.sYear.prev(sYear)] for (sST_Res,sVin) in m.sST_Res*m.sVin if (sST_Res,sES_Res) in m.sQSTOUT_Res if (sVin,m.sYear.prev(sYear)) in m.sVinYear)
        else:
            return  m.vSTNewCapRes [sST_Res,sYear] <= sum(m.pSTInsCap [sST_Res,sVin]                     for sVin in m.sVin if (sST_Res,sES_Res) in m.sQSTOUT_Res if (sVin,             sYear)  in m.sVinYear) + m.pTCMax * sum(m.pSTInsCap [sST_Res,sVin]                     for (sST_Res,sVin) in m.sST_Res*m.sVin if (sST_Res,sES_Res) in m.sQSTOUT_Res if (sVin,             sYear)  in m.sVinYear)
    #GWh
    d['EQ_TC_Res']                  = Constraint(m.sQSTOUT_Oth, m.sYear,        rule = EQ_TC_Res,           doc = '[ST units]')
    
    
    # Energy Services (ES)-related constraints
    
    # Transpotration
    def EQ_ESBalanceTra         (m,sST_Tra,sES_Tra,sYear,sSeason,sDay,sHour        ):
        return       sum(m.vQSTOut_Tra [sST_Tra,sES_Tra,sVin,sYear,sSeason,sDay,sHour] for (_,sVin) in m.sVinYear_indexed[sYear]) >= m.vQES_Tra [sST_Tra,sES_Tra,sYear] * m.pESLoadTra[sES_Tra,sSeason,sDay,sHour] #- m.vQESNS [sST,sES,sYear,sSeason,sDay,sHour]
    #ES units
    d['EQ_ESBalance']            = Constraint(m.sQSTOUT_Tra,m.sTime,         rule = EQ_ESBalanceTra,           doc = 'Balance for ES Tra [ES units]')
    
    # Industry balance
    def EQ_ESBalanceInd         (m,sST_Ind,sES_Ind,sYear,sSeason,sDay,sHour        ):
        return       sum(m.vQSTOut_Ind [sST_Ind,sES_Ind,sVin,sYear,sSeason,sDay,sHour] for (_,sVin) in m.sVinYear_indexed[sYear]) >= m.vQES_Ind [sST_Ind,sES_Ind,sYear] * m.pESLoadInd[sES_Ind,sSeason,sDay,sHour]
    #ES units
    d['EQ_ESBalanceInd']            = Constraint(m.sQSTOUT_Ind,m.sTime,         rule = EQ_ESBalanceInd,           doc = 'Balance for ES Ind [ES units]')
    
    # Oth balance
    def EQ_ESBalanceOth         (m,sST_Oth,sES_Oth,sYear,sSeason,sDay,sHour        ):
        return       sum(m.vQSTOut_Oth [sST_Oth,sES_Oth,sVin,sYear,sSeason,sDay,sHour] for (_,sVin) in m.sVinYear_indexed[sYear]) >= m.vQES_Oth [sST_Oth,sES_Oth,sYear] * m.pESLoadOth[sES_Oth,sSeason,sDay,sHour]
    #ES units
    d['EQ_ESBalanceOth']            = Constraint(m.sQSTOUT_Oth,m.sTime,         rule = EQ_ESBalanceOth,           doc = 'Balance for ES Oth [ES units]')

    # Residential balance
    def EQ_ESBalanceRes         (m,sST_Res,sES_Res,sSD_Res,sMD_Res,sYear,sSeason,sDay,sHour        ):
        return       sum(m.vQSTOut_Res [sST_Res,sES_Res,sSD_Res,sMD_Res,sVin,sYear,sSeason,sDay,sHour] for (_,sVin) in m.sVinYear_indexed[sYear]) >= m.vQES_Res [sST_Res,sES_Res,sSD_Res,sMD_Res,sYear] * m.pESLoadRes[sES_Res,sSD_Res,sMD_Res,sSeason,sDay,sHour]  ## Necesitaré una curva de carga para cada ES Residencial?
    #ES units
    d['EQ_ESBalanceRes']            = Constraint(m.sQSTOUT_Res,m.sTime,         rule = EQ_ESBalanceRes,           doc = 'Balance for ES Res [ES units]')
    # Demand-related constraints
    
    #Industry
    
    ##RM consumption
    def EQ_STBalanceRM         (m,sRM,sST_Ind,sES_Ind,sVin,sYear,sSeason,sDay,sHour        ):
        return  m.vQSTInRM [sRM,sST_Ind,sES_Ind,sVin,sYear,sSeason,sDay,sHour]  >= m.vQSTOut_Ind [sST_Ind,sES_Ind,sVin,sYear,sSeason,sDay,sHour] * m.pSTEffRM[sRM,sST_Ind,sES_Ind]
    #ES units
    d['EQ_STBalanceRM']      = Constraint(m.sQSTInRM,m.sVinTime,     rule = EQ_STBalanceRM,     doc = 'Balance for ST consumption of RM [RM units]')
    
    
    ##AF
    def EQ_AFInd         (m,sSD_Ind,sYear        ):
        return sum((m.vQES_Ind [sST_Ind,sES_Ind,sYear] * m.pAFInd[sES_Ind,sSD_Ind]) for (_,sES_Ind,sST_Ind) in m.sQSTOUT_AFInd_indexed[sSD_Ind]) >= m.vQSDInd[sSD_Ind,sYear]
    #Mt
    d['EQ_AFInd']            = Constraint(m.sSD_Ind,m.sYear,         rule = EQ_AFInd,           doc = 'Activity Factor Industry [SD units]')
    
    
    ##DC
    def EQ_DCInd         (m,sMD_Ind,sYear        ):
        return sum((m.vQSDInd[sSD_Ind,sYear] * m.pDC[sSD_Ind,sMD_Ind]) for sSD_Ind in m.sSD_Ind if ((sSD_Ind,sMD_Ind) in m.sQSDMD)) >= m.pMD[sMD_Ind,sYear]
    #Mt
    d['EQ_DCInd']            = Constraint(m.sMD_Ind,m.sYear,         rule = EQ_DCInd,           doc = 'Demand characterization Industry [MD units]')
    
    
    ## Circularity constraint
    def EQ_CircularityInd         (m,sRM,sST,sES,sYear,sSeason,sDay,sHour        ):
        return sum(m.vQSTOut [sST,sES,sVin,sYear,sSeason,sDay,sHour] for (sST,sVin) in m.sST_Ind*m.sVin if ((sST,sES) in m.sQSTOUT_Ind and (sVin,sYear) in m.sVinYear)) >= sum(m.vQSTInRM [sRM,sST,sES,sVin,sYear,sSeason,sDay,sHour] for sVin in m.sVin if (sVin,sYear) in m.sVinYear) / m.pRMCircular[sES,sRM]
    #Mt
    d['EQ_CircularityInd']   = Constraint(m.sQSTInRM_Cir,m.sTime,    rule = EQ_CircularityInd,   doc = 'Circularity constraintis [RM units]')
    

    # Endogenous behavioural measures
    
    
    #Transportation
    
    ##AF
    def EQ_AFTra         (m,sSD_Tra,sYear       ):
        return   sum((m.vQES_Tra[sST_Tra,sES_Tra,sYear] * m.pAFTra[sST_Tra,sES_Tra,sSD_Tra]) for (_,sES_Tra,sST_Tra) in m.sQSTOUT_AFTra_indexed[sSD_Tra]) + sum( sum(m.vBMTra[sST_Tra,sES_Tra,sSD_Tra,sBM_Tra,sYear] for (_,sES_Tra,sST_Tra) in m.sQSTOUT_AFTra_indexed[sSD_Tra]) for sBM_Tra in m.sBM_Tra) >= m.vQSDTra [sSD_Tra,sYear]
    # SD units (Mpkm)
    d['EQ_AFTra']            = Constraint(m.sSD_Tra,m.sYear,                        rule = EQ_AFTra,           doc = 'Activity factor Transportation [SD units]')
    
    
    
    ##BM
    def EQ_BMTra         (m,sST_Tra,sES_Tra,sSD_Tra,sBM_Tra,sYear       ):
        return   m.vBMTra[sST_Tra,sES_Tra,sSD_Tra,sBM_Tra,sYear] <= m.pDeltaAFTra[sST_Tra,sES_Tra,sSD_Tra,sBM_Tra] * m.vQES[sST_Tra,sES_Tra,sYear]
    # SD units (Mpkm)
    d['EQ_BMTra']            = Constraint(m.sQSTESSD_Tra,m.sBM_Tra,m.sYear,         rule = EQ_BMTra,           doc = 'Behavioural Measures in Transportation [ES units]')
    
    
    
    ##DC
    def EQ_DCTra         (m,sSD_Tra,sYear       ):
        return   m.vQSDTra [sSD_Tra,sYear] >= sum(m.pDC[sSD_Tra,sMD_Tra] * m.pMD[sMD_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra]) - sum(sum(m.vDMTra[sSD_Tra,sMD_Tra,sDM_Tra,sYear] for (_,sMD_Tra) in m.sQSDMD_Tra_indexed[sSD_Tra]) for sDM_Tra in m.sDM_Tra)
    # SD units
    d['EQ_DCTra']            = Constraint(m.sSD_Tra,m.sYear,                        rule = EQ_DCTra,           doc = 'Demand characterization Transportation [SD units]')
    
    
    
    ##DM
    def EQ_DMTra         (m,sSD_Tra,sMD_Tra,sDM_Tra,sYear       ):
        return   m.vDMTra[sSD_Tra,sMD_Tra,sDM_Tra,sYear] <= m.pDeltaDC[sSD_Tra,sMD_Tra,sDM_Tra] * m.pMD[sMD_Tra,sYear]
    #
    d['EQ_DMTra']            = Constraint(m.sQSDMD_Tra,m.sDM_Tra,m.sYear,           rule = EQ_DMTra,           doc = 'Demand shift Measures in Transportation [MD units]')

    #Others
    
    ##AF
    def EQ_AFRes         (m,sES_Res,sYear        ):
        return     (sum((m.vQES    [sST_Res,sES_Res,sYear])                                     for (_,sST_Res)         in m.sQSTOUT_AFRes_indexed[sES_Res]) 
             >=     sum((m.vQSRes [sSD_Res,sMD_Res,sYear] * m.pAFRes[sES_Res,sSD_Res,sMD_Res]) for (_,sSD_Res,sMD_Res) in m.sQSDMD_Res_indexed   [sES_Res])  
             -  sum(sum(m.vBMOth   [sES_Res,sSD_Res,sMD_Res,sBM_Res,sYear] for (_,sSD_Res,sMD_Res) in m.sQSDMD_Res_indexed[sES_Res])  for sBM_Res in m.sBM_Res) 
             +  sum(sum(m.vBMOth_WAMAC     [sSD_Res,sMD_Res,sBM_Res,sYear] for (  sSD_Res,sMD_Res) in m.sQSDMD_Res)                   for sBM_Res in m.sBM_Res if sES_Res == 'sES_DSOTH_RES_WAMAC') 
             +  sum(sum(m.vBMOth_DIWAC     [sSD_Res,sMD_Res,sBM_Res,sYear] for (  sSD_Res,sMD_Res) in m.sQSDMD_Res)                   for sBM_Res in m.sBM_Res if sES_Res == 'sES_DSOTH_RES_DIWAC')
             +      sum(m.vBMOth_TW[sES_Res,sSD_Res,sMD_Res,        sYear] for (_,sSD_Res,sMD_Res) in m.sQSDMD_Res_indexed[sES_Res]))
    # ES units
    d['EQ_AFOth']            = Constraint(m.sES_Res,m.sYear,                        rule = EQ_AFRes,           doc = 'Activity factor Others [ES units]')
    
    
    
    ##BM
    def EQ_BMRes         (m,sES_Res,sSD_Res,sMD_Res,sBM_Res,sYear       ):
        return   m.vBMRes[sES_Res,sSD_Res,sMD_Res,sBM_Res,sYear] <= m.pDeltaAFOth[sES_Res,sSD_Res,sMD_Res,sBM_Res] * m.vQSDRes [sSD_Res,sMD_Res,sYear]
    # SD units ()
    d['EQ_BMRes']            = Constraint(m.sQESSDMD_Res,m.sBM_Oth,m.sYear,         rule = EQ_BMRes,           doc = 'Behavioural Measures in Others [SD units]')
    
        

    ######################################################################################################################################################################
    ######################################################################################################################################################################

    ######################################################################################################################################################################
    ######################################################################################################################################################################
 

    ##BM
    def EQ_BMRes_WAMA         (m,sSD_Res,sMD_Res,sBM_Res,sYear       ):
        return   m.vBMRes['sES_DSOTH_RES_WAMAH',sSD_Res,sMD_Res,sBM_Res,sYear] == - m.vBMRes_WAMAC  [sSD_Res,sMD_Res,sBM_Res,sYear]
    # SD units ()
    d['EQ_BMRes_WAMA']       = Constraint(m.sQSDMD_Res,m.sBM_Res,m.sYear,           rule = EQ_BMRes_WAMA,      doc = 'Behavioural Measures in Others. Washing Machines [SD units]')
    
    
    ##BM
    def EQ_BMRes_DIWA         (m,sSD_Res,sMD_Res,sBM_Res,sYear       ):
        return   m.vBMRes['sES_DSOTH_RES_DIWAH',sSD_Res,sMD_Res,sBM_Res,sYear] == - m.vBMRes_DIWAC  [sSD_Res,sMD_Res,sBM_Res,sYear]
    # SD units ()
    d['EQ_BMRes_DIWA']       = Constraint(m.sQSDMD_Res,m.sBM_Res,m.sYear,           rule = EQ_BMRes_DIWA,      doc = 'Behavioural Measures in Others. Dish Washers [SD units]')
    
    
    ##BM
    def EQ_BMRes_TW         (m,sES_Res,sSD_Res,sMD_Res,sYear       ):
        return   m.vBMRes_TW[sES_Res,sSD_Res,sMD_Res,sYear] == m.pTW [sES_Res,sSD_Res,sMD_Res] * sum(m.vDMTra[sSD_Tra,sMD_Tra,'sDM_Tra_TW',sYear] for (sSD_Tra,sMD_Tra) in m.sQSDMD_Tra)
    # SD units ()
    d['EQ_BMRes_TW']         = Constraint(m.sQESSDMD_Res,m.sYear,                   rule = EQ_BMRes_TW,        doc = 'Behavioural Measures in Others. Telework [SD units]')
    
    
    
    #DC
    def EQ_DCOth         (m,sSD_Res,sMD_Res,sYear       ):
        return  m.vQSDRes [sSD_Res,sMD_Res,sYear] >= m.pDC[sSD_Res,sMD_Res] * m.pMD[sMD_Res,sYear] + (sum(m.vDMRes_HE[sMD_Res,sDM_Res,sYear] for sDM_Res in m.sDM_Res if sSD_Res in m.sSD_Res_HE) - sum(m.vDMRes_LE[sMD_Res,sDM_Res,sYear] for sDM_Res in m.sDM_Res if sSD_Res in m.sSD_Res_LE)) 
    # SD units: MDwellings or km2
    d['EQ_DCOth']            = Constraint(m.sQSDMD_Oth,m.sYear,                     rule = EQ_DCOth,           doc = 'Demand characterization Others [SD units]')
    
    
    
    ##DM
    def EQ_DMOth         (m,sMD_Oth,sDM_Oth,sYear       ):
        return   m.vDMOth_HE[sMD_Oth,sDM_Oth,sYear] <= sum(m.pDeltaDC[sSD_Oth,sMD_Oth,sDM_Oth] * m.pMD[sMD_Oth,sYear] for sSD_Oth in m.sSD_Oth_HE if (sSD_Oth,sMD_Oth) in m.sQSDMD_Oth)
    #
    d['EQ_DMOth']            = Constraint(m.sMD_Oth,m.sDM_Oth,m.sYear,              rule = EQ_DMOth,           doc = 'Demand shift Measures in Others [SD units]')
    
    
    
    ##DM
    def EQ_DMOth2         (m,sMD_Oth,sDM_Oth,sYear       ):
        return   m.vDMOth_HE[sMD_Oth,sDM_Oth,sYear] == m.vDMOth_LE[sMD_Oth,sDM_Oth,sYear]
    #
    d['EQ_DMOth2']            = Constraint(m.sMD_Oth,m.sDM_Oth,m.sYear,             rule = EQ_DMOth2,          doc = 'Demand shift Measures in Others [SD units]')
    
    
    
    ##DM
    def EQ_DMOth3         (m,sMD_Oth,sDM_Oth,sYear       ):
        if sYear>m.sYear.first(): 
            return   m.vDMOth_HE[sMD_Oth,sDM_Oth,sYear] >= m.vDMOth_HE[sMD_Oth,sDM_Oth,m.sYear.prev(sYear)] 
        else:
            return Constraint.Skip
    #
    d['EQ_DMOth3']            = Constraint(m.sMD_Oth,m.sDM_Oth,m.sYear,             rule = EQ_DMOth3,          doc = 'Demand shift Measures in Others [SD units]')
    
    
    # Conversion Energy (CE) capacity constraints
    
    
    def EQ_CEMaxPro_Pri         (m, sCEPri,sYear,sSeason,sDay,sHour        ):
        return m.vCEActCap [sCEPri,sYear] * m.pNumHours * m.pTimeSlice [sSeason,sDay,sHour] * m.pCEAF [sCEPri,sSeason,sDay,sHour]  >=  (m.vCEEleReserv [sCEPri,sYear,sSeason,sDay,sHour] if sCEPri in m.sCE_Ele else 0) + sum(m.vQCEPriOUT [sCEPri,sTE,sYear,sSeason,sDay,sHour] for (_,sTE) in m.sQCEPriOUT_CE_indexed[sCEPri])
    #GWh
    d['EQ_CEMaxPro_Pri']            = Constraint(m.sCEPri,m.sTime,         rule = EQ_CEMaxPro_Pri,           doc = 'CE maximum production (sCEPri) [GWh]')
    
    
    def EQ_CEMaxPro_Sec         (m, sCESec,sYear,sSeason,sDay,sHour        ):
        return m.vCEActCap [sCESec,sYear] * m.pNumHours * m.pTimeSlice [sSeason,sDay,sHour] * m.pCEAF [sCESec,sSeason,sDay,sHour]  >=  (m.vCEEleReserv [sCESec,sYear,sSeason,sDay,sHour] if sCESec in m.sCE_Ele else 0) + sum(m.vQCESecOUT [sCESec,sTE,sYear,sSeason,sDay,sHour] for (_,sTE) in m.sQCESecOUT_CE_indexed[sCESec])
    #GWh
    d['EQ_CEMaxPro_Sec']            = Constraint(m.sCESec,m.sTime,         rule = EQ_CEMaxPro_Sec,           doc = 'CE maximum production (sCESec) [GWh]')
    
    
    def EQ_CEMaxPro_Sto         (m, sCESto,sYear,sSeason,sDay,sHour        ):
        return m.vCEActCap [sCESto,sYear] * m.pNumHours * m.pTimeSlice [sSeason,sDay,sHour] * m.pCEAF [sCESto,sSeason,sDay,sHour]  >=  (m.vCEEleReserv [sCESto,sYear,sSeason,sDay,sHour] if sCESto in m.sCE_Ele else 0) + sum(m.vQCEStoOUT [sCESto,sTE,sYear,sSeason,sDay,sHour] for (_,sTE) in m.sQCEStoOUT_CE_indexed[sCESto])
    #GWh
    d['EQ_CEMaxPro_Sto']            = Constraint(m.sCESto,m.sTime,         rule = EQ_CEMaxPro_Sto,           doc = 'CE maximum production (sCESto) [GWh]')
    
    
    def EQ_CEMaxCap         (m, sCE,sYear        ):
        return m.pCEMaxCap [sCE]  >=  m.vCETotCap [sCE,sYear]
    #GW
    d['EQ_CEMaxCap']                = Constraint(m.sCE,m.sYear,            rule = EQ_CEMaxCap,               doc = 'CE maximum capacity [GW]')
    
    
    def EQ_CEInsCap         (m, sCE,sYear        ):
        return m.vCETotCap [sCE,sYear] == (m.vCETotCap[sCE,m.sYear.prev(sYear)] if sYear>m.sYear.first() else ((1-m.pGreenfield) * m.pCEInsCap[sCE])) + (m.vCENewCap [sCE,sYear]) - (m.vCEDecCap [sCE,sYear])
    #GW
    d['EQ_CEInsCap']                = Constraint(m.sCE,m.sYear,            rule = EQ_CEInsCap,               doc = 'CE installed capacity [GW]')
    
    
    def EQ_CEDecCap         (m, sCE,sYear        ):
        return m.vCEDecCap [sCE,sYear]  ==  (
            ((1-m.pGreenfield) * m.pYrGap * (m.pCEInsCap[sCE]/m.pCELife[sCE])      if ((m.sYear.ord(sYear) <= (m.pCELife[sCE]/m.pYrGap)) and (not sCE in (m.sCE_Hydro))) else 0)
            + (m.vCENewCap[sCE,m.sYear.prev(sYear, m.pCELife[sCE]//int(m.pYrGap))] if   m.sYear.ord(sYear) >  (m.pCELife[sCE]/m.pYrGap)                                  else 0)
                                            )
    #GW    
    d['EQ_CEDecCap']                = Constraint(m.sCE,m.sYear,            rule = EQ_CEDecCap,               doc = 'CE decommissioned capacity [GW]')
    
    
    def EQ_CEActCap         (m, sCE,sYear         ):
        return m.vCEActCap [sCE,sYear]  == m.vCETotCap [sCE,sYear] - m.vCEHibCap [sCE, sYear]
    #GW
    d['EQ_CEActCap']                = Constraint(m.sCE,m.sYear,            rule = EQ_CEActCap,               doc = 'CE active capacity [GW]')
    
    
    def EQ_CEReactCap         (m, sCE,sYear        ):
        return m.vCEDeltaActCap [sCE,sYear]  >=  - m.vCEHibCap [sCE, sYear] + (m.vCEHibCap [sCE, m.sYear.prev(sYear)]  if (not sYear==m.sYear.first())  else 0) - m.vCEDecCap[sCE,sYear]
    #GW
    d['EQ_CEReactCap']              = Constraint(m.sCE, m.sYear,           rule = EQ_CEReactCap,             doc = 'Reactivation of CE capacity [GW]')
    
    
    
    def EQ_CEEleReserv         (m, sYear,sSeason,sDay,sHour        ):
        return sum(m.vCEEleReserv [sCE_Ele,sYear,sSeason,sDay,sHour] * m.pCEFlex [sCE_Ele] for sCE_Ele in m.sCE_Ele) >= (    m.pCEFailCap
                                                                                                                      + sum((m.vQSTInTE [sTE,sST,sES,sVin,sYear,sSeason,sDay,sHour]/(m.pNumHours * m.pTimeSlice [sSeason,sDay,sHour])) for (_,_,_,_,sTE,sST,sES,sVin) in m.sTESTESVinTime_Ele_indexed[sYear,sSeason,sDay,sHour]) * m.pCEDemErr
                                                                                                                      + sum( m.vCEActCap[sCE_Var,sYear] * m.pCEAF [sCE_Var,sSeason,sDay,sHour] for  sCE_Var      in  m.sCE_Var) * m.pCEAFErr
                                                                                                                        )   
    #GW
    d['EQ_CEEleReserv']             = Constraint(m.sTime,                  rule = EQ_CEEleReserv,            doc = 'Reserves for electricity generation [GW]')
    
    
    
    def EQ_EleMaxDem         (m, sYear,sSeason,sDay,sHour         ):
        return m.vEleMaxDem [sYear]  >= sum((m.vQSTInTE [sTE,sST,sES,sVin,sYear,sSeason,sDay,sHour]/(m.pNumHours * m.pTimeSlice [sSeason,sDay,sHour])) for (_,_,_,_,sTE,sST,sES,sVin)     in  m.sTESTESVinTime_Ele_indexed[sYear,sSeason,sDay,sHour])
    #GW 
    d['EQ_EleMaxDem']               = Constraint(m.sTime,                  rule = EQ_EleMaxDem,              doc = 'Yearly maximum electricity power demand [GW]')
      
    
    
    def EQ_CEEleAdeq         (m, sYear         ):
        return sum(m.vCEActCap [sCE_Ele,sYear] * m.pCEFirm [sCE_Ele] for sCE_Ele in m.sCE_Ele) >= (1 + m.pCEResMar) * m.vEleMaxDem [sYear]
    #GW
    d['EQ_CEEleAdeq']               = Constraint(m.sYear,                  rule = EQ_CEEleAdeq,              doc = 'Adequacy for electricity generation [GW]')
    
    
    def EQ_NucCap         (m, sCE_Nuc,sYear        ):
        return (m.pCEInsCap[sCE_Nuc] if m.sYear.ord(sYear)<len(m.sYearNuc) else 0) >= m.vCEActCap[sCE_Nuc,sYear] 
    #GW    
    d['EQ_NucCap']                  = Constraint(m.sCE_Nuc,m.sYear,        rule = EQ_NucCap,                 doc = 'Nuclear dismantling restriction [GW]')
    
    
    def EQ_CoalCap         (m, sCE_Coal,sYear        ):
        return (m.pCEInsCap[sCE_Coal] if m.sYear.ord(sYear)<len(m.sYearCoal) else 0) >= m.vCEActCap[sCE_Coal,sYear] 
    #GW  
    d['EQ_CoalCap']                 = Constraint(m.sCE_Coal,m.sYear,       rule = EQ_CoalCap,                doc = 'Coal phase-out restriction [GW]')
    
    
    # Supply Technologies (ST) capacity constraints
    
    
    def EQ_STMaxProCap         (m, sST_Cap,sVin,sYear,sSeason,sDay,sHour        ):
        return m.vSTTotCap [sST_Cap,sVin,sYear] * m.pNumHours * m.pTimeSlice [sSeason,sDay,sHour] >=  sum(m.vQSTOut [sST_Cap,sES,sVin,sYear,sSeason,sDay,sHour] for (_,sES) in m.sQSTOUT_sST_Cap[sST_Cap])
    #GWh
    d['EQ_STMaxProCap']            = Constraint(m.sST_Cap,m.sVinTime,         rule = EQ_STMaxProCap,           doc = 'ST maximum production [ES units]')
    
    
    def EQ_STMaxProUni         (m, sST_Uni,sVin,sYear        ):
        return m.vSTTotCap [sST_Uni,sVin,sYear] * m.pSTMaxPro[sST_Uni] >=  sum(m.vQSTOut [sST_Uni,sES,sVin,sYear,sSeason,sDay,sHour] for (_,sES,sSeason,sDay,sHour) in m.sQSTOUT_sST_Uni[sST_Uni])
    #GWh
    d['EQ_STMaxProUni']            = Constraint(m.sST_Uni,m.sVinYear,         rule = EQ_STMaxProUni,           doc = 'ST maximum production per unit [ES units]')
    
    
    '''
    #def EQ_STMaxCap         (m, sST,sYear        ):
    #    return m.pSTMaxCap [sST]  >=  sum(m.vSTTotCap [sST,sVin,sYear] for sVin in m.sVin if (sVin,sYear) in m.sVinYear)
    #GW
    #d['EQ_STMaxCap']              = Constraint(m.sST,m.sYear,                rule = EQ_STMaxCap,              doc = 'ST maximum capacity [ST units]')
    '''
    
    
    def EQ_STInsCap         (m, sST,sVin,sYear        ):
        return m.vSTTotCap [sST,sVin,sYear]  == ((1-m.pGreenfield) * m.pSTInsCap[sST,sVin] if sYear==m.sYear.first() else 0) + (m.vSTTotCap[sST,sVin,m.sYear.prev(sYear)] if (sYear>m.sYear.first() and m.pYr[sYear]>m.pYr[sVin]) else 0) + (m.vSTNewCap [sST,sYear] if m.pYr[sYear]==m.pYr[sVin] else 0) - (m.vSTDecCap [sST,sVin,sYear] if m.pYr[sYear]>m.pYr[sVin] else 0)
    #GW
    d['EQ_STInsCap']               = Constraint(m.sST,m.sVinYear,             rule = EQ_STInsCap,              doc = 'ST installed capacity [ST units]')
    
    
    def EQ_STDecCap         (m, sST,sVin,             sYear ): 
        return m.vSTDecCap  [   sST,sVin,             sYear ]  ==  (
             ((m.vSTTotCap  [   sST,sVin,m.sYear.prev(sYear)] if sYear>m.sYear.first() else (1-m.pGreenfield)*m.pSTInsCap[sST,sVin]) if m.pYr[sYear]>m.pYr[sVin] else 0) * sum(m.pSTDecProb[sST,sAge] for sAge in m.sAge if m.sAge.ord(sAge)==m.pYr[sYear]-m.pYr[sVin]))                              
    #GW    
    d['EQ_STDecCap']               = Constraint(m.sST,m.sVinYear,             rule = EQ_STDecCap,              doc = 'ST decommissioned capacity [ST units]')
    
    
    # ### Emissions accounting
    
    # CO2 emissions
    
    
    ##CE
    
    def EQ_EmiCO2CEPri         (m, sPE,sCEPri,sYear        ):
        return   m.vEmiCO2CEPri[sPE,sCEPri,sYear] == m.pEmiCO2CEPri[sPE,sCEPri] * sum(m.vQCEPriIN [sPE,sCEPri,sYear,sSeason,sDay,sHour] for (_,_,_,sSeason,sDay,sHour) in m.sQCEPriIN_YTime_indexed[sPE,sCEPri,sYear])    
    #ktCO2                                              
    d['EQ_EmiCO2CEPri']            = Constraint(m.sQCEPriIN,m.sYear,        rule = EQ_EmiCO2CEPri,           doc = 'CO2 emissions in Primary CE processes [ktCO2]')
    
    
    def EQ_EmiCO2CESec         (m, sTE,sCESec,sYear        ):
        return   m.vEmiCO2CESec[sTE,sCESec,sYear] == m.pEmiCO2CESec[sTE,sCESec] * sum(m.vQCESecIN [sTE,sCESec,sYear,sSeason,sDay,sHour] for (_,_,_,sSeason,sDay,sHour) in m.sQCESecIN_YTime_indexed[sTE,sCESec,sYear]) 
    #ktCO2                                              
    d['EQ_EmiCO2CESec']            = Constraint(m.sQCESecIN,m.sYear,        rule = EQ_EmiCO2CESec,           doc = 'CO2 emissions in Secondary CE processes [ktCO2]')
    
    
    def EQ_EmiCO2CESto         (m, sTE,sCESto,sYear        ):
        return   m.vEmiCO2CESto[sTE,sCESto,sYear] == m.pEmiCO2CESto[sTE,sCESto] * sum(m.vQCEStoIN[sTE,sCESto,sYear,sSeason,sDay,sHour] for (_,_,_,sSeason,sDay,sHour) in m.sQCEStoIN_YTime_indexed[sTE,sCESto,sYear])  
    #ktCO2                                              
    d['EQ_EmiCO2CESto']            = Constraint(m.sQCEStoIN,m.sYear,        rule = EQ_EmiCO2CESto,           doc = 'CO2 emissions in Storage CE processes [ktCO2]')
    
    def EQ_EmiCO2CE         (m, sCE,sYear        ):
        return   m.vEmiCO2CE[sCE,sYear] == sum(m.vEmiCO2CEPri[sPE,sCE,sYear] for (_,sPE) in m.sQCEPriIN_CE_indexed[sCE]) +  sum(m.vEmiCO2CESec[sTE,sCE,sYear] for (_,sTE) in m.sQCESecIN_CE_indexed[sCE]) +  sum(m.vEmiCO2CESto[sTE,sCE,sYear] for (_,sTE) in m.sQCEStoIN_CE_indexed[sCE])
    #ktCO2                                              
    d['EQ_EmiCO2CE']               = Constraint(m.sCE,m.sYear,              rule = EQ_EmiCO2CE,              doc = 'CO2 emissions in CE processes [ktCO2]')
    
    
    ##TE
    
    def EQ_EmiCO2TE         (m, sTE,sYear        ):
        return   m.vEmiCO2TE[sTE,sYear] ==  m.pEmiCO2TE[sTE] * (sum(m.vQSTInTE[sTE,sST,sES,sVin,sYear,sSeason,sDay,sHour]  for (_,_,sST,sES,sVin,sSeason,sDay,sHour) in m.sSTESVinTime_indexed[sTE,sYear])  + sum(m.vQTELoss[sTE,sYear,sSeason,sDay,sHour] for (sSeason,sDay,sHour) in m.sYearTime)) 
    #ktCO2
    d['EQ_EmiCO2TE']               = Constraint(m.sTE,m.sYear,              rule = EQ_EmiCO2TE,              doc = 'CO2 emissions in TE transportation [ktCO2]')
    
    ##ST
    
    
    def EQ_EmiCO2STTE         (m,sTE,sST,sES,sYear        ):
        return   m.vEmiCO2STTE[sTE,sST,sES,sYear] ==  m.pEmiCO2STTE[sST,sTE] * (sum(m.vQSTInTE[sTE,sST,sES,sVin,sYear,sSeason,sDay,sHour]  for (_,_,_,_,sVin,sSeason,sDay,sHour) in m.sSTESTESVinTime_indexed[sTE,sST,sES,sYear]))  
    #ktCO2   
    d['EQ_EmiCO2STTE']             = Constraint(m.sQTESTES,m.sYear,         rule = EQ_EmiCO2STTE,            doc = 'CO2 emissions in ST due to TE consumption [ktCO2]')
    
    
    def EQ_EmiCO2STPro         (m,sST,sES,sYear       ):
        return   m.vEmiCO2STPro[sST,sES,sYear] ==  m.pEmiCO2STPro[sST,sES] * (sum(m.vQSTOut[sST,sES,sVin,sYear,sSeason,sDay,sHour]  for (_,_,_,sVin,sSeason,sDay,sHour) in m.sQSTOUT_ST_ES_Year_indexed[sST,sES,sYear]))/1e3  
    #ktCO2   
    d['EQ_EmiCO2STPro']            = Constraint(m.sQSTOUT,m.sYear,          rule = EQ_EmiCO2STPro,           doc = 'CO2 emissions in ST due to TE consumption [ktCO2]')
    
    
    def EQ_EmiCO2ST         (m, sST,sES,sYear        ):
        return   m.vEmiCO2ST[sST,sES,sYear] == sum(m.vEmiCO2STTE[sTE,sST,sES,sYear] for (_,_,sTE) in m.sQTESTES_STES_indexed[sST,sES]) + m.vEmiCO2STPro[sST,sES,sYear]
    #ktCO2                                              
    d['EQ_EmiCO2ST']               = Constraint(m.sQSTOUT,m.sYear,          rule = EQ_EmiCO2ST,              doc = 'CO2 emissions in ST [ktCO2]')
    
    ##ESNS
    
    def EQ_EmiCO2ESNS         (m, sYear        ):
        return   m.vEmiCO2ESNS [sYear]  ==  m.pEmiCO2ESNS * sum(m.vQESNS[sST,sES,sYear,sSeason,sDay,sHour] for (_,sST,sES,sSeason,sDay,sHour) in m.sQSTOUT_Time_indexed[sYear]) 
    #ktCO2   
    d['EQ_EmiCO2ESNS']             = Constraint(m.sYear,                    rule = EQ_EmiCO2ESNS,            doc = 'CO2 penalization emissions related to ENS (TE consumption and CE process) [ktCO2]')
    
    
    ##Total
     
    def EQ_EmiCO2Tot         (m, sYear        ):
        return   m.vEmiCO2Tot [sYear]  ==  (sum(m.vEmiCO2CE [sCE,sYear] for sCE in m.sCE) + sum(m.vEmiCO2TE [sTE,sYear] for sTE in m.sTE) + sum(m.vEmiCO2ST [sST,sES,sYear] for (sST,sES) in m.sQSTOUT))/1e3 #+ m.vEmiCO2ESNS[sYear])/1e3
    #MtCO2
    d['EQ_EmiCO2Tot']              = Constraint(m.sYear,                    rule = EQ_EmiCO2Tot,             doc = 'Total CO2 emissions [MtCO2]')
    
    
    # NOx emissions
    
    
    #NOx Emissions
    
    ##CE
    
    
    def EQ_EmiNOxCEPri         (m, sPE,sCEPri,sYear        ):
        return   m.vEmiNOxCEPri[sPE,sCEPri,sYear] == m.pEmiNOxCEPri[sPE,sCEPri] * sum(m.vQCEPriIN [sPE,sCEPri,sYear,sSeason,sDay,sHour] for (_,_,_,sSeason,sDay,sHour) in m.sQCEPriIN_YTime_indexed[sPE,sCEPri,sYear])    
    #tNOx                                              
    d['EQ_EmiNOxCEPri']            = Constraint(m.sQCEPriIN,m.sYear,        rule = EQ_EmiNOxCEPri,           doc = 'NOx emissions in Primary CE processes [tNOx]')
    
    
    def EQ_EmiNOxCESec         (m, sTE,sCESec,sYear        ):
        return   m.vEmiNOxCESec[sTE,sCESec,sYear] == m.pEmiNOxCESec[sTE,sCESec] * sum(m.vQCESecIN [sTE,sCESec,sYear,sSeason,sDay,sHour] for (_,_,_,sSeason,sDay,sHour) in m.sQCESecIN_YTime_indexed[sTE,sCESec,sYear]) 
    #tNOx                                              
    d['EQ_EmiNOxCESec']            = Constraint(m.sQCESecIN,m.sYear,        rule = EQ_EmiNOxCESec,           doc = 'NOx emissions in Secondary CE processes [tNOx]')
    
    
    def EQ_EmiNOxCESto         (m, sTE,sCESto,sYear        ):
        return   m.vEmiNOxCESto[sTE,sCESto,sYear] == m.pEmiNOxCESto[sTE,sCESto] * sum(m.vQCEStoIN[sTE,sCESto,sYear,sSeason,sDay,sHour] for (_,_,_,sSeason,sDay,sHour) in m.sQCEStoIN_YTime_indexed[sTE,sCESto,sYear])  
    #tNOx                                              
    d['EQ_EmiNOxCESto']            = Constraint(m.sQCEStoIN,m.sYear,        rule = EQ_EmiNOxCESto,           doc = 'NOx emissions in Storage CE processes [tNOx]')
    
    
    def EQ_EmiNOxCE         (m, sCE,sYear        ):
        return   m.vEmiNOxCE[sCE,sYear] == (sum(m.vEmiNOxCEPri[sPE,sCE,sYear] for (_,sPE) in m.sQCEPriIN_CE_indexed[sCE]) +  sum(m.vEmiNOxCESec[sTE,sCE,sYear] for (_,sTE) in m.sQCESecIN_CE_indexed[sCE]) +  sum(m.vEmiNOxCESto[sTE,sCE,sYear] for (_,sTE) in m.sQCEStoIN_CE_indexed[sCE]))*1e-3
    #ktNOx                                              
    d['EQ_EmiNOxCE']               = Constraint(m.sCE,m.sYear,              rule = EQ_EmiNOxCE,              doc = 'NOx emissions in CE processes [tNOx]')
    
    
    ##ST
    
    def EQ_EmiNOxSTTE         (m,sTE,sST,sES,sYear        ):
        return   m.vEmiNOxSTTE[sTE,sST,sES,sYear] ==  m.pEmiNOxSTTE[sST,sTE] * (sum(m.vQSTInTE[sTE,sST,sES,sVin,sYear,sSeason,sDay,sHour]  for (_,_,_,_,sVin,sSeason,sDay,sHour) in m.sSTESTESVinTime_indexed[sTE,sST,sES,sYear]))  
    #tNOx   
    d['EQ_EmiNOxSTTE']             = Constraint(m.sQTESTES,m.sYear,         rule = EQ_EmiNOxSTTE,           doc = 'NOx emissions in ST due to TE consumption [tNOx]')
    
    
    def EQ_EmiNOxSTPro         (m,sST,sES,sYear       ):
        return   m.vEmiNOxSTPro[sST,sES,sYear] ==  m.pEmiNOxSTPro[sST,sES] * (sum(m.vQSTOut[sST,sES,sVin,sYear,sSeason,sDay,sHour]  for (_,_,_,sVin,sSeason,sDay,sHour) in m.sQSTOUT_ST_ES_Year_indexed[sST,sES,sYear]))  
    #tNOx   
    d['EQ_EmiNOxSTPro']            = Constraint(m.sQSTOUT,m.sYear,          rule = EQ_EmiNOxSTPro,          doc = 'NOx emissions in ST due to TE consumption [tNOx]')
    
    
    def EQ_EmiNOxST         (m, sST,sES,sYear        ):
        return   m.vEmiNOxST[sST,sES,sYear] == (sum(m.vEmiNOxSTTE[sTE,sST,sES,sYear] for (_,_,sTE) in m.sQTESTES_STES_indexed[sST,sES]) + m.vEmiNOxSTPro[sST,sES,sYear])*1e-3
    #ktNOx                                              
    d['EQ_EmiNOxST']               = Constraint(m.sQSTOUT,m.sYear,          rule = EQ_EmiNOxST,             doc = 'NOx emissions in ST [ktNOx]')
    
    
    ##ESNS
    
    def EQ_EmiNOxESNS         (m, sYear        ):
        return   m.vEmiNOxESNS [sYear]  ==  m.pEmiNOxESNS * sum(m.vQESNS[sST,sES,sYear,sSeason,sDay,sHour] for (_,sST,sES,sSeason,sDay,sHour) in m.sQSTOUT_Time_indexed[sYear])*1e-3 
    #ktNOx   
    d['EQ_EmiNOxESNS']             = Constraint(m.sYear,                    rule = EQ_EmiNOxESNS,           doc = 'NOx penalization emissions related to ENS (TE consumption and CE process) [ktNOx]')
    
    
    ##Total
     
    def EQ_EmiNOxTot         (m, sYear        ):
        return   m.vEmiNOxTot [sYear]  ==  (sum(m.vEmiNOxCE [sCE,sYear] for sCE in m.sCE) + sum(m.vEmiNOxST [sST,sES,sYear] for (sST,sES) in m.sQSTOUT) + m.vEmiNOxESNS[sYear])*1e-3
    #MtNOx
    d['EQ_EmiNOxTot']              = Constraint(m.sYear,                    rule = EQ_EmiNOxTot,            doc = 'Total NOx emissions [MtNOx]')
    
    
    
    # SOx emissions
    
    
    ##CE
    
    def EQ_EmiSOxCEPri         (m, sPE,sCEPri,sYear        ):
        return   m.vEmiSOxCEPri[sPE,sCEPri,sYear] == m.pEmiSOxCEPri[sPE,sCEPri] * sum(m.vQCEPriIN [sPE,sCEPri,sYear,sSeason,sDay,sHour] for (_,_,_,sSeason,sDay,sHour) in m.sQCEPriIN_YTime_indexed[sPE,sCEPri,sYear])    
    #tSOx                                              
    d['EQ_EmiSOxCEPri']            = Constraint(m.sQCEPriIN,m.sYear,        rule = EQ_EmiSOxCEPri,           doc = 'SOx emissions in Primary CE processes [tSOx]')
    
    
    def EQ_EmiSOxCESec         (m, sTE,sCESec,sYear        ):
        return   m.vEmiSOxCESec[sTE,sCESec,sYear] == m.pEmiSOxCESec[sTE,sCESec] * sum(m.vQCESecIN [sTE,sCESec,sYear,sSeason,sDay,sHour] for (_,_,_,sSeason,sDay,sHour) in m.sQCESecIN_YTime_indexed[sTE,sCESec,sYear]) 
    #tSOx                                              
    d['EQ_EmiSOxCESec']            = Constraint(m.sQCESecIN,m.sYear,        rule = EQ_EmiSOxCESec,           doc = 'SOx emissions in Secondary CE processes [tSOx]')
    
    
    def EQ_EmiSOxCESto         (m, sTE,sCESto,sYear        ):
        return   m.vEmiSOxCESto[sTE,sCESto,sYear] == m.pEmiSOxCESto[sTE,sCESto] * sum(m.vQCEStoIN[sTE,sCESto,sYear,sSeason,sDay,sHour] for (_,_,_,sSeason,sDay,sHour) in m.sQCEStoIN_YTime_indexed[sTE,sCESto,sYear])  
    #tSOx                                              
    d['EQ_EmiSOxCESto']            = Constraint(m.sQCEStoIN,m.sYear,        rule = EQ_EmiSOxCESto,           doc = 'SOx emissions in Storage CE processes [tSOx]')
    
    def EQ_EmiSOxCE         (m, sCE,sYear        ):
        return   m.vEmiSOxCE[sCE,sYear] == (sum(m.vEmiSOxCEPri[sPE,sCE,sYear] for (_,sPE) in m.sQCEPriIN_CE_indexed[sCE]) +  sum(m.vEmiSOxCESec[sTE,sCE,sYear] for (_,sTE) in m.sQCESecIN_CE_indexed[sCE]) +  sum(m.vEmiSOxCESto[sTE,sCE,sYear] for (_,sTE) in m.sQCEStoIN_CE_indexed[sCE]))*1e-3
    #ktSOx                                              
    d['EQ_EmiSOxCE']               = Constraint(m.sCE,m.sYear,              rule = EQ_EmiSOxCE,              doc = 'SOx emissions in CE processes [ktSOx]')
    
    
    ##ST
    
    def EQ_EmiSOxSTTE         (m,sTE,sST,sES,sYear        ):
        return   m.vEmiSOxSTTE[sTE,sST,sES,sYear] ==  m.pEmiSOxSTTE[sST,sTE] * (sum(m.vQSTInTE[sTE,sST,sES,sVin,sYear,sSeason,sDay,sHour]  for (_,_,_,_,sVin,sSeason,sDay,sHour) in m.sSTESTESVinTime_indexed[sTE,sST,sES,sYear]))  
    #tSOx   
    d['EQ_EmiSOxSTTE']             = Constraint(m.sQTESTES,m.sYear,         rule = EQ_EmiSOxSTTE,            doc = 'SOx emissions in ST due to TE consumption [tSOx]')
    
    
    def EQ_EmiSOxSTPro         (m,sST,sES,sYear       ):
        return   m.vEmiSOxSTPro[sST,sES,sYear] ==  m.pEmiSOxSTPro[sST,sES] * (sum(m.vQSTOut[sST,sES,sVin,sYear,sSeason,sDay,sHour]  for (_,_,_,sVin,sSeason,sDay,sHour) in m.sQSTOUT_ST_ES_Year_indexed[sST,sES,sYear]))  
    #tSOx   
    d['EQ_EmiSOxSTPro']            = Constraint(m.sQSTOUT,m.sYear,          rule = EQ_EmiSOxSTPro,           doc = 'SOx emissions in ST due to TE consumption [kSOx]')
    
    
    def EQ_EmiSOxST         (m, sST,sES,sYear        ):
        return   m.vEmiSOxST[sST,sES,sYear] == (sum(m.vEmiSOxSTTE[sTE,sST,sES,sYear] for (_,_,sTE) in m.sQTESTES_STES_indexed[sST,sES]) + m.vEmiSOxSTPro[sST,sES,sYear])*1e-3
    #ktSOx                                              
    d['EQ_EmiSOxST']               = Constraint(m.sQSTOUT,m.sYear,          rule = EQ_EmiSOxST,              doc = 'SOx emissions in ST [ktSOx]')
    
    
    ##ESNS
    
    def EQ_EmiSOxESNS         (m, sYear        ):
        return   m.vEmiSOxESNS [sYear]  ==  m.pEmiSOxESNS * sum(m.vQESNS[sST,sES,sYear,sSeason,sDay,sHour] for (_,sST,sES,sSeason,sDay,sHour) in m.sQSTOUT_Time_indexed[sYear])*1e-3 
    #ktSOx   
    d['EQ_EmiSOxESNS']             = Constraint(m.sYear,                    rule = EQ_EmiSOxESNS,            doc = 'SOx penalization emissions related to ENS (TE consumption and CE process) [ktSOx]')
    
    
    ##Total
     
    def EQ_EmiSOxTot         (m, sYear        ):
        return   m.vEmiSOxTot [sYear]  ==  (sum(m.vEmiSOxCE [sCE,sYear] for sCE in m.sCE) + sum(m.vEmiSOxST [sST,sES,sYear] for (sST,sES) in m.sQSTOUT) + m.vEmiSOxESNS[sYear])*1e-3
    #MtSOx
    d['EQ_EmiSOxTot']              = Constraint(m.sYear,                    rule = EQ_EmiSOxTot,             doc = 'Total SOx emissions [MtSOx]')
    
    
    # PM 2.5 emissions
    
    
    ##CE
    
    def EQ_EmiPM25CEPri         (m, sPE,sCEPri,sYear        ):
        return   m.vEmiPM25CEPri[sPE,sCEPri,sYear] == m.pEmiPM25CEPri[sPE,sCEPri] * sum(m.vQCEPriIN [sPE,sCEPri,sYear,sSeason,sDay,sHour] for (_,_,_,sSeason,sDay,sHour) in m.sQCEPriIN_YTime_indexed[sPE,sCEPri,sYear])    
    #tPM25                                              
    d['EQ_EmiPM25CEPri']            = Constraint(m.sQCEPriIN,m.sYear,        rule = EQ_EmiPM25CEPri,           doc = 'PM25 emissions in Primary CE processes [tPM25]')
    
    
    
    def EQ_EmiPM25CESec         (m, sTE,sCESec,sYear        ):
        return   m.vEmiPM25CESec[sTE,sCESec,sYear] == m.pEmiPM25CESec[sTE,sCESec] * sum(m.vQCESecIN [sTE,sCESec,sYear,sSeason,sDay,sHour] for (_,_,_,sSeason,sDay,sHour) in m.sQCESecIN_YTime_indexed[sTE,sCESec,sYear]) 
    #tPM25                                              
    d['EQ_EmiPM25CESec']            = Constraint(m.sQCESecIN,m.sYear,        rule = EQ_EmiPM25CESec,           doc = 'PM25 emissions in Secondary CE processes [tPM25]')
    
    
    
    def EQ_EmiPM25CESto         (m, sTE,sCESto,sYear        ):
        return   m.vEmiPM25CESto[sTE,sCESto,sYear] == m.pEmiPM25CESto[sTE,sCESto] * sum(m.vQCEStoIN[sTE,sCESto,sYear,sSeason,sDay,sHour] for (_,_,_,sSeason,sDay,sHour) in m.sQCEStoIN_YTime_indexed[sTE,sCESto,sYear])  
    #tPM25                                              
    d['EQ_EmiPM25CESto']            = Constraint(m.sQCEStoIN,m.sYear,        rule = EQ_EmiPM25CESto,           doc = 'PM25 emissions in Storage CE processes [tPM25]')
    
    def EQ_EmiPM25CE         (m, sCE,sYear        ):
        return   m.vEmiPM25CE[sCE,sYear] == (sum(m.vEmiPM25CEPri[sPE,sCE,sYear] for (_,sPE) in m.sQCEPriIN_CE_indexed[sCE]) +  sum(m.vEmiPM25CESec[sTE,sCE,sYear] for (_,sTE) in m.sQCESecIN_CE_indexed[sCE]) +  sum(m.vEmiPM25CESto[sTE,sCE,sYear] for (_,sTE) in m.sQCEStoIN_CE_indexed[sCE]))*1e-3
    #ktPM25                                              
    d['EQ_EmiPM25CE']               = Constraint(m.sCE,m.sYear,              rule = EQ_EmiPM25CE,              doc = 'PM25 emissions in CE processes [ktPM25]')
    
    
    ##ST
    
    
    def EQ_EmiPM25STTE         (m,sTE,sST,sES,sYear        ):
        return   m.vEmiPM25STTE[sTE,sST,sES,sYear] ==  m.pEmiPM25STTE[sST,sTE] * (sum(m.vQSTInTE[sTE,sST,sES,sVin,sYear,sSeason,sDay,sHour]  for (_,_,_,_,sVin,sSeason,sDay,sHour) in m.sSTESTESVinTime_indexed[sTE,sST,sES,sYear]))  
    #tPM25   
    d['EQ_EmiPM25STTE']             = Constraint(m.sQTESTES,m.sYear,         rule = EQ_EmiPM25STTE,            doc = 'PM25 emissions in ST due to TE consumption [tPM25]')
    
    
    def EQ_EmiPM25STPro         (m,sST,sES,sYear       ):
        return   m.vEmiPM25STPro[sST,sES,sYear] ==  m.pEmiPM25STPro[sST,sES] * (sum(m.vQSTOut[sST,sES,sVin,sYear,sSeason,sDay,sHour]  for (_,_,_,sVin,sSeason,sDay,sHour) in m.sQSTOUT_ST_ES_Year_indexed[sST,sES,sYear]))  
    #tPM25   
    d['EQ_EmiPM25STPro']            = Constraint(m.sQSTOUT,m.sYear,          rule = EQ_EmiPM25STPro,           doc = 'PM25 emissions in ST due to TE consumption [tPM25]')
    
    
    def EQ_EmiPM25ST         (m, sST,sES,sYear        ):
        return   m.vEmiPM25ST[sST,sES,sYear] == (sum(m.vEmiPM25STTE[sTE,sST,sES,sYear] for (_,_,sTE) in m.sQTESTES_STES_indexed[sST,sES]) + m.vEmiPM25STPro[sST,sES,sYear])*1e-3
    #ktPM25                                              
    d['EQ_EmiPM25ST']               = Constraint(m.sQSTOUT,m.sYear,          rule = EQ_EmiPM25ST,              doc = 'PM25 emissions in ST [ktPM25]')
    
    
    ##ESNS
    
    
    def EQ_EmiPM25ESNS         (m, sYear        ):
        return   m.vEmiPM25ESNS [sYear]  ==  m.pEmiPM25ESNS * sum(m.vQESNS[sST,sES,sYear,sSeason,sDay,sHour] for (_,sST,sES,sSeason,sDay,sHour) in m.sQSTOUT_Time_indexed[sYear])*1e-3 
    #ktPM25   
    d['EQ_EmiPM25ESNS']             = Constraint(m.sYear,                    rule = EQ_EmiPM25ESNS,            doc = 'PM25 penalization emissions related to ENS (TE consumption and CE process) [ktPM25]')
    
    
    ##Total
    
     
    def EQ_EmiPM25Tot         (m, sYear        ):
        return   m.vEmiPM25Tot [sYear]  ==  (sum(m.vEmiPM25CE [sCE,sYear] for sCE in m.sCE) + sum(m.vEmiPM25ST [sST,sES,sYear] for (sST,sES) in m.sQSTOUT) + m.vEmiPM25ESNS[sYear])*1e-3
    #MtPM25
    d['EQ_EmiPM25Tot']              = Constraint(m.sYear,                    rule = EQ_EmiPM25Tot,             doc = 'Total PM25 emissions [MtPM25]')
    
    
    # ### Emission limits
    
    
    ##Cap
    
    def EQ_EmiCO2Cap         (m, sYear        ):
        return   m.pEmiCO2Cap [sYear]  >=  m.vEmiCO2Tot [sYear] - m.vEmiCO2CapExc [sYear]
    #MtCO2
    d['EQ_EmiCO2Cap']            = Constraint(m.sYear,        rule = EQ_EmiCO2Cap,           doc = 'Emission cap restriction [MtCO2]')
    
    
    def EQ_EmiNOxCap         (m, sYear        ):
        return   m.pEmiNOxCap [sYear]  >=  m.vEmiNOxTot [sYear] - m.vEmiNOxCapExc [sYear]
    #MtNOx
    d['EQ_EmiNOxCap']            = Constraint(m.sYear,        rule = EQ_EmiNOxCap,           doc = 'Emission cap restriction [MtNOx]')
    
    
    def EQ_EmiSOxCap         (m, sYear        ):
        return   m.pEmiSOxCap [sYear]  >=  m.vEmiSOxTot [sYear] - m.vEmiSOxCapExc [sYear]
    #MtSOx
    d['EQ_EmiSOxCap']            = Constraint(m.sYear,        rule = EQ_EmiSOxCap,           doc = 'Emission cap restriction [MtSOx]')
    
    
    def EQ_EmiPM25Cap         (m, sYear        ):
        return   m.pEmiPM25Cap [sYear]  >=  m.vEmiPM25Tot [sYear] - m.vEmiPM25CapExc [sYear]
    #MtPM25
    d['EQ_EmiPM25Cap']           = Constraint(m.sYear,        rule = EQ_EmiPM25Cap,          doc = 'Emission cap restriction [MtPM25]')
    
    
    
    ##Carbon budget
    
    def EQ_EmiCO2Budget         (m        ):
        return   m.pEmiCO2Budget  >=  m.pYrGap * sum(m.vEmiCO2Tot[sYear] for sYear in m.sYear)- m.vEmiCO2BudgetExc
    #MtCO2
    d['EQ_EmiCO2Budget']         = Constraint(                rule = EQ_EmiCO2Budget,        doc = 'Emission budget restriction for the Before Net-zero target year period [MtCO2]')
    
    
    
    
    # CO2 sectorial emissions limits
    
    
    ## Transport
    def EQ_EmiCO2CapTra         (m, sYear        ):
        return    m.pEmiCO2CapTra [sYear] >=  sum(m.vEmiCO2ST [sST_Tra,sES_Tra,sYear] for (sST_Tra,sES_Tra) in m.sQSTOUT_Tra)*1e-3 - m.vEmiCO2CapTraExc [sYear]
    #MtCO2
    d['EQ_EmiCO2CapTra']            = Constraint(m.sYear,        rule = EQ_EmiCO2CapTra,           doc = 'Transport emission cap restriction [MtCO2]')
    
    
    
    ## Electric generation
    def EQ_EmiCO2CapEle         (m, sYear        ):
        return    m.pEmiCO2CapEle [sYear] >= sum(m.vEmiCO2CE [sCE_Ele,sYear] for sCE_Ele in m.sCE_Ele)*1e-3 - m.vEmiCO2CapEleExc [sYear]
    #MtCO2
    d['EQ_EmiCO2CapEle']            = Constraint(m.sYear,        rule = EQ_EmiCO2CapEle,           doc = 'Electricity generation emission cap restriction [MtCO2]')
    
    
    ## Industrial sector (energy)
    def EQ_EmiCO2CapIndTE       (m, sYear        ):
        return    m.pEmiCO2CapIndTE [sYear] >= sum(m.vEmiCO2STTE[sTE,sST_Ind,sES_Ind,sYear] for (sTE,sST_Ind,sES_Ind) in m.sQTESTES_Ind)*1e-3 - m.vEmiCO2CapIndTEExc [sYear]
    #MtCO2
    d['EQ_EmiCO2CapIndTE']            = Constraint(m.sYear,        rule = EQ_EmiCO2CapIndTE,           doc = 'Energy-related industrial emission cap restriction [MtCO2]')
    
    
    
    ## Industrial sector (process)
    def EQ_EmiCO2CapIndPro      (m, sYear        ):
        return    m.pEmiCO2CapIndPro [sYear] >= sum(m.vEmiCO2STPro[sST_Ind,sES_Ind,sYear] for (sST_Ind,sES_Ind) in m.sQSTOUT_Ind)*1e-3 - m.vEmiCO2CapIndProExc [sYear]
    #MtCO2
    d['EQ_EmiCO2CapIndPro']           = Constraint(m.sYear,        rule = EQ_EmiCO2CapIndPro,           doc = 'Process-related industrial emission cap restriction [MtCO2]')
    
    
    ## Residential and commercial
    def EQ_EmiCO2CapOth      (m, sYear        ):
        return    m.pEmiCO2CapOth [sYear] >= sum(m.vEmiCO2ST [sST_Oth,sES_Oth,sYear] for (sST_Oth,sES_Oth) in m.sQSTOUT_Oth)*1e-3 - m.vEmiCO2CapOthExc [sYear]
    #MtCO2
    d['EQ_EmiCO2CapOth']            = Constraint(m.sYear,        rule = EQ_EmiCO2CapOth,           doc = 'Residential&Commercial emission cap restriction [MtCO2]')
    
    
    ## Refine industry
    def EQ_EmiCO2CapRef         (m, sYear        ):
        return    m.pEmiCO2CapRef [sYear] >= sum(m.vEmiCO2CE [sCE_Ref,sYear] for sCE_Ref in m.sCE_Ref)*1e-3 - m.vEmiCO2CapRefExc [sYear]
    #MtCO2
    d['EQ_EmiCO2CapRef']            = Constraint(m.sYear,        rule = EQ_EmiCO2CapRef,           doc = 'Refinery production emission cap restriction [MtCO2]')

    l_eq = [
        'EQ_FObj',
        'EQ_SysCost',
        'EQ_PenalCost',
        'EQ_TotalCost',
        'EQ_BMCost',
        'EQ_DMCost',
        'EQ_InvCostCE',
        'EQ_InvCostST',
        'EQ_OpCost',
        'EQ_OpVarom',
        'EQ_PEDomCap',
        'EQ_PEImpCap',
        'EQ_PEBalance',
        'EQ_CEPriBalance',
        'EQ_CEPriOutShareMin',
        'EQ_CEPriOutShareMax',
        'EQ_CESecBalance',
        'EQ_CESecOutShareMin',
        'EQ_CESecOutShareMax',
        'EQ_CEStoBalance',
        'EQ_CEStoLevel',
        'EQ_CEStoOutShareMin',
        'EQ_CEStoOutShareMax',
        'EQ_CEStoMaxSto',
        'EQ_TEBalance',
        'EQ_TELoss',
        'EQ_STBalanceTE_Tra',
        'EQ_STBalanceTE_Oth',
        'EQ_STBalanceTE_Ind',
        'EQ_STOutShareMin',
        'EQ_STOutShareMax',
        'EQ_MinMS_Car',
        'EQ_MinMS_Bus',
        'EQ_MinMS_Moped',
        'EQ_MinMS_IntRail',
        'EQ_MinMS_UrbanRail',
        'EQ_MinMS_Air',
        'EQ_MinMS_Sea',
        'EQ_MaxMS_Car',
        'EQ_MaxMS_Bus',
        'EQ_MaxMS_Moped',
        'EQ_MaxMS_IntRail',
        'EQ_MaxMS_UrbanRail',
        'EQ_MaxMS_Air',
        'EQ_MaxMS_Sea',
        #'EQ_TC_Car',
        #'EQ_TC_Moped',
        #'EQ_TC_RoadFreight',
        #'EQ_TC_Bus',
        #'EQ_TC_UrbanRail',
        #'EQ_TC_IntRail',
        #'EQ_TC_Air',    
        #'EQ_TC_Sea',    
        #'EQ_TC_Oth',
        'EQ_ESBalance',
        'EQ_AFTra',
        'EQ_BMTra',
        'EQ_DCTra',
        'EQ_DMTra',
        'EQ_AFOth',
        'EQ_BMOth',
        'EQ_BMOth_WAMA',
        'EQ_BMOth_DIWA',
        'EQ_BMOth_TW',
        'EQ_DCOth',
        'EQ_DMOth',
        'EQ_DMOth2',
        'EQ_DMOth3',
        'EQ_STBalanceRM',
        'EQ_AFInd',
        'EQ_DCInd',
        'EQ_CircularityInd',
        'EQ_CEMaxPro_Pri',
        'EQ_CEMaxPro_Sec',
        'EQ_CEMaxPro_Sto',
        'EQ_CEMaxCap',
        'EQ_CEInsCap',
        'EQ_CEDecCap',
        'EQ_CEActCap',
        'EQ_CEReactCap',
        'EQ_CEEleReserv',
        'EQ_EleMaxDem',
        'EQ_CEEleAdeq',
        'EQ_NucCap',
        'EQ_CoalCap',
        'EQ_STMaxProCap',
        'EQ_STMaxProUni',
        #'EQ_STMaxCap',
        'EQ_STInsCap',
        'EQ_STDecCap',
        'EQ_EmiCO2CEPri',
        'EQ_EmiCO2CESec',
        'EQ_EmiCO2CESto',
        'EQ_EmiCO2CE',
        'EQ_EmiCO2TE',
        'EQ_EmiCO2STTE',
        'EQ_EmiCO2STPro',
        'EQ_EmiCO2ST',
        #'EQ_EmiCO2ESNS',
        'EQ_EmiCO2Tot',
        'EQ_EmiNOxCEPri',
        'EQ_EmiNOxCESec',
        'EQ_EmiNOxCESto',
        'EQ_EmiNOxCE',
        'EQ_EmiNOxSTTE',
        'EQ_EmiNOxSTPro',
        'EQ_EmiNOxST',
        'EQ_EmiNOxESNS',
        'EQ_EmiNOxTot',
        'EQ_EmiSOxCEPri',
        'EQ_EmiSOxCESec',
        'EQ_EmiSOxCESto',
        'EQ_EmiSOxCE',
        'EQ_EmiSOxSTTE',
        'EQ_EmiSOxSTPro',
        'EQ_EmiSOxST',
        'EQ_EmiSOxESNS',
        'EQ_EmiSOxTot',
        'EQ_EmiPM25CEPri',
        'EQ_EmiPM25CESec',
        'EQ_EmiPM25CESto',
        'EQ_EmiPM25CE',
        'EQ_EmiPM25STTE',
        'EQ_EmiPM25STPro',
        'EQ_EmiPM25ST',
        'EQ_EmiPM25ESNS',
        'EQ_EmiPM25Tot',
        'EQ_EmiCO2Cap',
        'EQ_EmiNOxCap',
        'EQ_EmiSOxCap',
        'EQ_EmiPM25Cap',
        'EQ_EmiCO2Budget',
        'EQ_EmiCO2CapTra',
        'EQ_EmiCO2CapEle',
        'EQ_EmiCO2CapIndTE',
        'EQ_EmiCO2CapIndPro',
        'EQ_EmiCO2CapOth',
        'EQ_EmiCO2CapRef',
    ]
    for eq in l_eq:
        setattr(m, eq, d[eq])

    return m
