import moltbook

mb = moltbook.Moltbook()
try:
    res = mb._request("GET", "/submolts/memory")
    print(res)
except Exception as e:
    print("Error:", e)
