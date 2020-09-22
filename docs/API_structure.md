## PARKING LOT APIs:
---------------------

* Details important to take the action will be in the body of the APIs
* Make changes to APIs on the fly if needed according to designed LLD and ER diagrams
### POST /enter/{floorNo}/{entryNo}
<pre>
Request Body: 
                {
                    customerName:
                    customerVehicleType:
                    customerVehicleNumber:
                    customerAddress:
                    cutomerMobileNo:
                }
Response Body:
                {
                    status:
                    ticketNo:
                    isBlacklisted:
                }
</pre>
### POST /exit/{floorNo}/{exitNo}
<pre>
Request Body:
                {
                    customerVehicleNumber:
                    ticketNo:
                }
Response Body:
                {
                    status:
                    isPaid:
                }
</pre>
### GET /isPaid/{ticketNo}
<pre>
Request Body:
                {}
Response Body:
                {
                    status:
                    customerVehicleNumber:
                    isPaid:
                }
</pre>
### GET /amountToPay/{ticketNo}
<pre>
Request Body:
                {}
Response Body:
                {
                    status:
                    customerVehicleNumber:
                    amount:
                }
</pre>
### GET /pay
<pre>
Request Body:
                {
                    ticketNo:
                    amount:
                    mode:
                    boothId:
                }
Response Body:
                {
                    status:
                    isPaid:
                }
</pre>

### GET /displayMessage/{floorNo}
<pre>
Request Body:
                {
                    isEntry: False implies exit
                    pathId: Basically entry id or exit id
                }
Response Body:
                {
                    status:
                    displayMessage:
                }
</pre>
### GET /slotsAvailable/{floorNo}
<pre>
Request Body:
                {}
Response Body:
                {
                    status:
                    slotsAvailable:
                }
</pre>
### POST /bookSlot/{floorNo}/{slotNo}
<pre>
Request Body:
                {}
Response Body:
                {
                    status:
                    isBooked:
                }
</pre>
### POST /freeSlot/{floorNo}/{slotNo}
<pre>
Request Body:
                {}
Response Body:
                {
                    status:
                    isFreed:
                }
</pre>

### GET /orientation/{floorNo}
<pre>
Request Body:
                {}
Response Body:
                {
                    status:
                    slots: [
                        {
                            slotId:
                            isBooked:
                        },
                        {
                            slotId:
                            isBooked:
                        }
                    ]
                }
</pre>

### POST /electricUseStart/{ticketNo}
<pre>
Request Body:
                {
                    timestampStart:
                }
Response Body:
                {
                    status:
                    isMarked:
                }
</pre>
### POST /electricUseStop/{ticketNo}
<pre>
Request Body:
                {
                    timestampStop:
                }
Response Body:
                {
                    status:
                    isMarked:
                }
</pre>

### GET /simulateTraffic/{loadFactor i.e. APM}
<pre>Design similar to /orientation/{floorNo}/</pre>

ADMIN:
------
* All APIs here with OAuth authenticator
### POST /addFloor
### PATCH /editFloor
### DELETE /removeFloor
### POST /addSlot
### PATCH /editSlot
### DELETE /removeSlot
### POST /addPA
### DELETE /removePA
### POST /addRate
### PATCH /editRate
### DELETE /removeRate