import time, requests, statistics as st
API="http://localhost:8000/ask"
Q="Explica brevemente qué es RAG y por qué ayuda a reducir alucinaciones."
N=10
lat=[]

for i in range(N):
    t0=time.time()
    r=requests.post(API, json={"question": Q}, timeout=300)
    r.raise_for_status()
    lat.append(time.time()-t0)
    print(f"{i+1}/{N} -> {lat[-1]:.2f}s")

print("Min:", min(lat), "Max:", max(lat), "Avg:", st.mean(lat), "P95:", st.quantiles(lat, n=20)[18])
