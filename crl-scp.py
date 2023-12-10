#!/usr/bin/env python3

# From this example:
# https://pydicom.github.io/pynetdicom/stable/tutorials/create_scp.html
#

import os

from pydicom.filewriter import write_file_meta_info

from pynetdicom import (
    AE, debug_logger, evt, AllStoragePresentationContexts,
     ALL_TRANSFER_SYNTAXES
)

debug_logger()

def handle_store(event, storage_dir):
    """Handle EVT_C_STORE events."""
    try:
      os.makedirs(storage_dir, exist_ok=True)
    except:
      # Unable to create output dir, return failure status
      return 0xC001

    # We rely on the UID from the C-STORE request instead of decoding
    print(event.request.AffectedSOPInstanceUID)
    print(event.request)
    filenamecomponent = event.request.AffectedSOPInstanceUID + '.dcm'
    fname = os.path.join(storage_dir, filenamecomponent)
    with open(fname, 'wb') as f:
        # Write the preamble, prefix and file meta information elements
        f.write(b'\x00' * 128)
        f.write(b'DICM')
        write_file_meta_info(f, event.file_meta)
        # Write the raw encoded dataset
        f.write(event.request.DataSet.getvalue())
    return 0x0000

handlers = [(evt.EVT_C_STORE, handle_store, ['out'])]

ae = AE()
storage_sop_classes = [
     cx.abstract_syntax for cx in AllStoragePresentationContexts
]

for uid in storage_sop_classes:
     ae.add_supported_context(uid, ALL_TRANSFER_SYNTAXES)

ae.start_server(("127.0.0.1", 11112), block=True, evt_handlers=handlers)


