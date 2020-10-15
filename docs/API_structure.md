## PARKING LOT APIs:
---------------------

* Details important to take the action will be in the body of the APIs
* Make changes to APIs on the fly if needed according to designed LLD and ER diagrams

### GET /getFreeSlots/{parkingLotID}/{floorNumber}/{vehicleType}
<pre>
Request Body:
                {}
Response Body:
                {
                    spotID: 
                    status: 
                    rowNumber:
                    columnNumber:
                }
</pre>

### POST /enter/customer/{parkingLotID}/{floorNumber}/{entryNoumber}/{spotID}
<pre>
Request Body:
                {
                    customerName:
                    customerVehicleType:
                    customerVehicleNumber:
                    cutomerMobileNo:
                }
Response Body:
                {
                    status: 
                    ticket': {
                                ticketNumber:
                                customerId:
                                vehicleNumber: 
                                inTime:
                              }
                }
</pre>
### POST /exit/customer/{ticketNumber}
<pre>
Request Body:
                {
                    parkingAttendantID:
                    parkingLotID:
                    floorNumber:
                    exitNumber:
                }
Response Body:
                {
                    status:
                    message:
                }
</pre>
### GET /isPaid/ticketNumber/{ticketNumber}
<pre>
Request Body:
                {}
Response Body:
                {
                    status:
                    isPaid:
                }
</pre>
### GET /isPaid/vehicleNumber/{vehicleNumber}
<pre>
Request Body:
                {}
Response Body:
                {
                    status:
                    isPaid:
                }
</pre>
### GET /getAmount/ticketNumber/{ticketNumber}
<pre>
Request Body:
                {}
Response Body:
                {
                    ticketNumber:
                    vehicleNumber:
                    totalParkingHours:
                    totalChargingHours: 
                    parkingFee: 
                    chargingFee: 
                    totalAmount:

                }
</pre>
### GET /getAmount/vehicleNumber/{vehicleNumber}
<pre>
Request Body:
                {}
Response Body:
                {
                    ticketNumber:
                    vehicleNumber:
                    totalParkingHours:
                    totalChargingHours: 
                    parkingFee: 
                    chargingFee: 
                    totalAmount:

                }
</pre>
### POST /pay
<pre>
Request Body:
                {
                    ticketNumber:
                    amount:
                    mode:
                }
Response Body:
                {
                    status:
                    isPaid:
                }
</pre>

### POST /displayMessage/{floorNo}
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
<!-- ### GET /slotsAvailable/{floorNo}
<pre>
Request Body:
                {}
Response Body:
                {
                    status:
                    slotsAvailable:
                }
</pre> -->
<!-- ### POST /bookSlot/{floorNo}/{slotNo}
<pre>
Request Body:
                {}
Response Body:
                {
                    status:
                    isBooked:
                }
</pre> -->
<!-- ### POST /freeSlot/{floorNo}/{slotNo}
<pre>
Request Body:
                {}
Response Body:
                {
                    status:
                    isFreed:
                }
</pre> -->

<!-- ### GET /orientation/{floorNo}
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
</pre> -->

### POST /electricUseStart/{ticketNo}
<pre>
Request Body:
                {                  
                }
Response Body:
                {
                    status:
                    message:
                }
</pre>
### POST /electricUseStop/{ticketNo}
<pre>
Request Body:
                {                   
                }
Response Body:
                {
                    status:
                    message:
                    duration:
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