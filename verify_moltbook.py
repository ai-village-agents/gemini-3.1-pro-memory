import moltbook

mb = moltbook.Moltbook()
try:
    res = mb._request("POST", "/verify", body={
        "verification_code": "moltbook_verify_ff15687ca9d9c1bb34948858888c5d99",
        "answer": "57.00"
    })
    print(res)
except Exception as e:
    print("Error:", e)
