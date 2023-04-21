New name idea: thermal_therapist

======================================

Idea of execution

Number of used TDAU's defined in .soc file: (2) 
TD1
TD2

Number of DIODE's defined in thermal bath file: (3) 
NAC
GPIO
PCH

Select which TDAU maps to which DIODE:
TD1 : 
> NAC
TD2 : 
> GPIO

Enter SDS and SDT temperature setpoints:
SDS : 
> -10
SDT : 
> 80

Exporting tdau xml setup...

========================================

1. There will always be a COLD + HOT section of the tdau xml,
2. The number of TDAUs will depend on no. defined in .soc

A list of length = no. tdaus x2 (COLD + HOT) will be created.
Each item in list will contain dict for each tdau/temp pair.
Realistically, four dicts, x2 tdaus x2 will be created, eg...

[tdau1_cold,  tdau2_cold, tdau1_cold, tdau1_hot] =
[
'diode'   : NAC, 
'tdau'    : THERMD_TD1,
'channel' : 1,
'slope'   : -602.23
'temp'    : -10,
'current' : [30,60,180],  
'ideality': 1.031,
,
'diode'   : NAC, 
'tdau'    : THERMD_TD1,
'channel' : 1,
'slope'   : -602.23
'temp'    : 80,
'current' : [30,60,180],  
'ideality': 1.031,
,
'diode'   : GPIO, 
'tdau'    : THERMD_TD1,
'channel' : 5,
'slope'   : -600.34
'temp'    : -10,
'current' : [30,60,180],  
'ideality': 1.031,
,
'diode'   : GPIO, 
'tdau'    : THERMD_TD1,
'channel' : 5,
'slope'   : -600.34
'temp'    : 80,
'current' : [30,60,180],  
'ideality': 1.031,
]
====================================

Structure of tdau xml is below.

COLD
    TD1
    TD2
HOT
    TD1
    TD2
