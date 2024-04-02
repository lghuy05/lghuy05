def DFS(u, parent, keo, adj_list):
    total_keo = 0
    for v in adj_list[u]:
        if v != parent:
            total_keo += DFS(v, u, keo, adj_list)
    return max(total_keo, 0) + keo[u]


n = int(input())
keo = list(map(int, input().split()))
adj_list = [[] for _ in range(n)]
for _ in range(n - 1):
    u, v = map(int, input().split())
    adj_list[u - 1].append(v - 1)
    adj_list[v - 1].append(u - 1)
s = int(input()) - 1

res = DFS(s, -1, keo, adj_list)
print(res)
