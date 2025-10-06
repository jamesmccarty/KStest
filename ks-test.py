import numpy as np
from scipy.stats import ks_2samp 
import matplotlib.pyplot as plt 
import argparse

# Written by J. McCarty

# parse command line arguments
parser = argparse.ArgumentParser(
	description="Two-sample KS test for comparing two sets of distance distributions from two MD simulations."
)
parser.add_argument(
	"-sample1", required=True, help="Path to the first distance data file."
)
parser.add_argument(
	"-sample2", required=True, help="Path to the second distance data file."
)
parser.add_argument(
	"-column", type=int, default=1, help="Column index (starts with 0) to read from each file (default is 1 for second column)."
)
parser.add_argument(
	"-noplot",action="store_true", help="If provided, skip plotting the CDFs (default: plot is shown)."
)
args = parser.parse_args()
# everything should be parsed by now
print("Will read column ",args.column+1, " from the data files")

# load two different sets of data:
sampleA = np.loadtxt(args.sample1, comments='#!', usecols=(args.column,))
sampleB = np.loadtxt(args.sample2, comments='#!', usecols=(args.column,))

# KS test:
ks_res = ks_2samp(sampleA, sampleB)

print(f"KS statistic = {ks_res.statistic:.4f}")
print(f"p-value = {ks_res.pvalue:.4e}")

if ks_res.pvalue < 0.05:
	print("statistically significant difference (distributions differ).")
else:
	print("No significant difference between distributions detected.")


# Optional: plot CDF
if not args.noplot:
	plot=True
else:
	plot=False

# plot=False
if(plot):
	
	# Sort the data for plotting CDF
	x_A = np.sort(sampleA)
	x_B = np.sort(sampleB)

	# CDF
	cdf_A = np.arange(1, len(x_A)+1)/ len(x_A)
	cdf_B = np.arange(1, len(x_B)+1)/ len(x_B)

	plt.plot(x_A, cdf_A)
	plt.plot(x_B, cdf_B)
	plt.ylabel("Cumulative Probability")
	plt.xlabel("x")
	plt.show()
