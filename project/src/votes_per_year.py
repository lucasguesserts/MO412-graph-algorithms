import matplotlib.pyplot as plt

plt.rcParams.update({"text.usetex": True, "font.family": "Helvetica"})


def plot_votes_per_year(years, votes):
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111)
    ax.plot(years, votes, color="k", linestyle="-", marker="o")
    ax.set_xlabel("year")
    ax.set_ylabel("number of votes")
    ax.grid(True)
    ax.set_xlim(min(*years), max(*years))
    fig.savefig("votes_per_year.png")
    plt.close()
