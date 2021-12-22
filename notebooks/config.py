input_path_exa = "/Users/Chris/Studies/thesis/experiment_results/exa/exp_exa_epsilon_h01_2/exp_exa_epsilon_h01_2_091.txt"
input_path_exa_2 = "/Users/Chris/Studies/thesis/experiment_results/exa/exp_exa_epsilon_h01_s3/exp_exa_epsilon_h01_s3_091.txt"
input_path_exa_3 = "/Users/Chris/Studies/thesis/experiment_results/exa/exp_exa_epsilon_h005_s3/exp_exa_epsilon_h005_s3_091.txt"
input_path_exa_driver_2 = (
    "/Users/Chris/Studies/thesis/experiment_results/exa/exp_exa_epsilon_h01_s3.txt"
)
input_path_exa_driver_3 = (
    "/Users/Chris/Studies/thesis/experiment_results/exa/exp_exa_epsilon_h005_s3.txt"
)
input_path_local = (
    "/Users/Chris/Studies/thesis/experiment_results/local/exp_local_epsilon_h01.txt"
)
input_path_spark = (
    "/Users/Chris/Studies/thesis/experiment_results/spark/exp_spark_epsilon_h01.txt"
)

input_path_url_exa = "/Users/Chris/Studies/thesis/experiment_results/exa/test.txt"
input_path_url_spark = (
    "/Users/Chris/Studies/thesis/experiment_results/spark/exp_spark_url_h1.txt"
)

base_path = "/Users/Chris/Studies/thesis/experiment_results/"

# Algorithm Performance
# Epsilon Dataset
alg_epsilon_local_path = base_path + "local/exp_local_epsilon_h1.txt"
alg_epsilon_spark_path = base_path + "spark/exp_spark_epsilon_h1.txt"
alg_epsilon_framework_path = (
    base_path + "exa/exp_exa_epsilon_h1/exp_exa_epsilon_h1_091.txt"
)
# URL Dataset
alg_url_local_path = base_path + "local/exp_local_url_h1.txt"
alg_url_spark_path = base_path + "spark/exp_spark_url_h1.txt"
alg_url_framework_path = base_path + "exa/exp_exa_url_h1/exp_exa_url_h1_091.txt"

# Communication Frequency
# Epsilon Dataset
comm_epsilon_spark_h01_path = base_path + "spark/exp_spark_epsilon_h01.txt"
comm_epsilon_spark_h1_path = base_path + "spark/exp_spark_epsilon_h1.txt"
comm_epsilon_framework_h1_path = (
    base_path + "exa/exp_exa_epsilon_h1_s3/exp_exa_epsilon_h1_090.txt"
)
comm_epsilon_framework_h05_path = (
    base_path + "exa/exp_exa_epsilon_h05_s3/exp_exa_epsilon_h05_s3_090.txt"
)
comm_epsilon_framework_h01_path = (
    base_path + "exa/exp_exa_epsilon_h01_s3/exp_exa_epsilon_h01_s3_090.txt"
)
comm_epsilon_framework_h005_path = (
    base_path + "exa/exp_exa_epsilon_h005_s3/exp_exa_epsilon_h005_s3_090.txt"
)
# URL Dataset
comm_url_spark_h01_path = base_path + "spark/exp_spark_url_h01.txt"
comm_url_spark_h1_path = base_path + "spark/exp_spark_url_h1.txt"
comm_url_framework_h1_path = base_path + "exa/exp_exa_url_h1/exp_exa_url_h1_091.txt"
comm_url_framework_h02_path = (
    base_path + "exa/exp_exa_url_h02_tap/exp_exa_url_h02_tap_091.txt"
)
comm_url_framework_h05_path = base_path + "exa/exp_exa_url_h05/exp_exa_url_h05_091.txt"

# Syncronization Strategy
# Epsilon
sst_epsilon_framework_bsp = (
    base_path + "exa/exp_exa_epsilon_h01/exp_exa_epsilon_h01_090.txt"
)
sst_epsilon_framework_ssp = (
    base_path + "exa/exp_exa_epsilon_h01_s3/exp_exa_epsilon_h01_s3_090.txt"
)
sst_epsilon_framework_tap = (
    base_path + "exa/exp_exa_epsilon_h01_tap/exp_exa_epsilon_h01_tap_090.txt"
)
# URL
sst_url_framework_bsp = base_path + "exa/exp_exa_url_h02/exp_exa_url_h02_091.txt"
sst_url_framework_ssp = base_path + "exa/exp_exa_url_h02_s3/exp_exa_url_h02_s3_091.txt"
sst_url_framework_tap = (
    base_path + "exa/exp_exa_url_h02_tap/exp_exa_url_h02_tap_087.txt"
)

# Merging Strategy
# Epsilon
merg_epsilon_add = (
    base_path + "exa/exp_exa_epsilon_h01_s3/exp_exa_epsilon_h01_s3_091.txt"
)
merg_epsilon_avg = (
    base_path + "exa/exp_exa_epsilon_h01_s3_avg/exp_exa_epsilon_h01_s3_avg_091.txt"
)
# URL
merg_url_add = base_path + "exa/exp_exa_url_h02_s3/exp_exa_url_h02_s3_091.txt"
merg_url_avg = base_path + "exa/exp_exa_url_h02_s3_avg/exp_exa_url_h02_s3_avg_091.txt"

# Filter Strategy
# URL
filt_url_baseline = base_path + "exa/exp_exa_url_h02_s3/exp_exa_url_h02_s3_091.txt"
filt_url_rr = base_path + "exa/exp_exa_url_h02_s3_rr/exp_exa_url_h02_s3_rr_091.txt"
filt_url_rnd = (
    base_path + "exa/exp_exa_url_h02_s3_rnd_2/exp_exa_url_h02_s3_rnd_2_091.txt"
)
filt_url_am = base_path + "exa/exp_exa_url_h02_s3_am/exp_exa_url_h02_s3_am_091.txt"
filt_url_rm = base_path + "exa/test7.txt"
