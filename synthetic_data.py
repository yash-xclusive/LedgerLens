import csv, json, os

def create_data(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    records = [
      {"record_id":"R001","name":"ABC Technologies Pvt Ltd","registration_id":"GSTIN-29ABC1234A1Z5","address":"12 MG Road Bengaluru"},
      {"record_id":"R002","name":"A.B.C. Technologies Private Limited","registration_id":"GSTIN-29ABC1234A1Z5","address":"12 Mahatma Gandhi Road Bengaluru"},
      {"record_id":"R003","name":"ABC Technology Services LLP","registration_id":"LLPIN-AAB-1234","address":"44 Residency Road Bengaluru"},
      {"record_id":"R004","name":"Northstar Components Limited","registration_id":"CIN-U12345KA2010PLC","address":"8 Industrial Area Chennai"},
      {"record_id":"R005","name":"North Star Component Ltd","registration_id":"CIN-U99999KA2012PLC","address":"91 Harbour Road Chennai"},
      {"record_id":"R006","name":"Blue River Logistics Pvt Ltd","registration_id":"GSTIN-27BLU9876B1Z2","address":"3 Port Road Mumbai"},
      {"record_id":"R007","name":"BlueRiver Logistics Private Limited","registration_id":"GSTIN-27BLU9876B1Z2","address":"3 Port Road Mumbai"},
      {"record_id":"R008","name":"Sunrise Retail Private Limited","registration_id":"GSTIN-33SUN2222C1Z8","address":"21 Market Street Hyderabad"},
      {"record_id":"R009","name":"Sunrise Retail Pvt Ltd","registration_id":"GSTIN-33SUN2222C1Z8","address":"21 Market St Hyderabad"},
      {"record_id":"R010","name":"Eastern Finance Services LLP","registration_id":"LLPIN-XYZ-5555","address":"6 Park Avenue Delhi"},
    ]
    transactions = [
      {"transaction_id":"T001","transaction_reference":"NEFT-1001","amount":50000,"entity_record_id":"R001"},
      {"transaction_id":"T002","transaction_reference":"NEFT-1002","amount":75000,"entity_record_id":"R004"},
      {"transaction_id":"T003","transaction_reference":"NEFT-1003","amount":50000,"entity_record_id":"R002"},
      {"transaction_id":"T004","transaction_reference":"NEFT-1003","amount":50000,"entity_record_id":"R002"},
      {"transaction_id":"T005","transaction_reference":"UPI-2001","amount":120000,"entity_record_id":"R006"},
      {"transaction_id":"T006","transaction_reference":"RTGS-3001","amount":8500,"entity_record_id":"R008"},
      {"transaction_id":"T007","transaction_reference":"RTGS-3002","amount":9100,"entity_record_id":"R009"},
      {"transaction_id":"T008","transaction_reference":"NEFT-4001","amount":225000,"entity_record_id":"R010"},
    ]
    with open(os.path.join(output_dir,"business_records.json"),"w") as f: json.dump(records,f,indent=2)
    with open(os.path.join(output_dir,"transactions.csv"),"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=transactions[0].keys()); w.writeheader(); w.writerows(transactions)
    return records, transactions

if __name__ == "__main__":
    create_data("data/synthetic")
