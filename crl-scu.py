#!/usr/bin/env python3

# From this example:
# https://pydicom.github.io/pynetdicom/stable/tutorials/create_scu.html
#
# SCU applications from pydicom include:
# storescu
# https://pydicom.github.io/pynetdicom/stable/apps/storescu.html
#   and
# echoscu
# https://pydicom.github.io/pynetdicom/stable/apps/echoscu.html
#
# Full applications include:
# storescp
# https://pydicom.github.io/pynetdicom/stable/apps/storescp.html
# 
# findscu
# movescu
# python -m pynetdicom movescu 127.0.0.1 11112 -k QueryRetrieveLevel=PATIENT -k PatientName= --store
#


from pynetdicom import AE, debug_logger

debug_logger()

ae = AE()
ae.add_requested_context('1.2.840.10008.1.1')
assoc = ae.associate("127.0.0.1", 11112)
if assoc.is_established:
    print('Association established with Echo SCP!')
    status = assoc.send_c_echo()
    assoc.release()
else:
    # Association rejected, aborted or never connected
    print('Failed to associate')

