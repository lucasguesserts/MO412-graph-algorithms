import pandas as pd

table_4_1_data = [
    # network, <k>, <k_in^2>, <k_out^2>, <k^2>
    ["internet", 6.34, None, None, 240.1],
    ["www", 4.60, 1_546.0, 482.4, None],
    ["power grid", 2.67, None, None, 10.3],
    ["mobile phone calls", 2.51, 12.0, 11.7, None],
    ["email", 1.81, 94.7, 1_163.9, None],
    ["science collaboration", 8.08, None, None, 178.2],
    ["actor network", 83.71, None, None, 47_353.7],
    ["citation network", 10.43, 971.5, 198.8, None],
    ["e. coli metabolism", 5.58, 535.7, 396.7, None],
    ["portein interactions", 2.90, None, None, 32.3],
]

def critical_threshold(k, k2):
    return 1 - (1 / ((k2 / k) - 1))

k = r"$\langle k \rangle$"
k_in = r"$\langle k_{in}^2 \rangle$"
k_out = r"$\langle k_{out}^2 \rangle$"
k_2 = r"$\langle k^2 \rangle$"
f_c_in = r"$f_{c, in}$"
f_c_out = r"$f_{c, out}$"
f_c_undirected = r"$f_{c}$"
f_c_directed = r"$f_{c, di}$"

df = pd.DataFrame(
    data=table_4_1_data,
    columns=["network", k, k_in, k_out, k_2],
)

df[f_c_undirected] = df.apply(
    lambda row: critical_threshold(row[k], row[k_2]), axis=1
)
df[f_c_in] = df.apply(lambda row: critical_threshold(row[k], row[k_in]), axis=1)
df[f_c_out] = df.apply(
    lambda row: critical_threshold(row[k], row[k_out]), axis=1
)
df[f_c_directed] = df.apply(lambda row: max(row[f_c_in], row[f_c_out]), axis=1)

print(df)

df.style\
    .hide(axis="index")\
    .format(precision=3, na_rep="-")\
    .to_latex(
        "result.tex",
        label="table:results",
        caption="networks and their properties.",
        position="H",
    )
