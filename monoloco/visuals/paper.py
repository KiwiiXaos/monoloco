# pylint: skip-file

import math
import itertools

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

from .printer import get_angle


def paper():
    """Print paper figures"""

    method = True
    task_error = True

    # Pull figure
    if method:
        fig_name = 'output_method.png'
        z_max = 5
        x_max = z_max * 25 / 30

        z_1 = 2
        z_2 = 4
        x_1 = 1
        x_2 = -2
        std_1 = 0.75
        std_2 = 1.5
        angle_1 = get_angle(x_1, z_1)
        angle_2 = get_angle(x_2, z_2)

        (x_1_down, x_1_up), (z_1_down, z_1_up) = get_confidence(x_1, z_1, std_1)
        (x_2_down, x_2_up), (z_2_down, z_2_up) = get_confidence(x_2, z_2, std_2)
        #
        # fig = plt.figure(0)
        # ax = fig.add_subplot(1, 1, 1)
        #
        # ell_1 = Ellipse((x_1, z_1), width=std_1 * 2, height=0.3, angle=angle_1, color='b', fill=False)
        #
        # ell_2 = Ellipse((x_2, z_2), width=std_2 * 2, height=0.3, angle=angle_2, color='b', fill=False)
        #
        # ax.add_patch(ell_1)
        # ax.add_patch(ell_2)
        # plt.plot(x_1_down, z_1_down, marker='o', markersize=8, color='salmon')
        # plt.plot(x_1, z_1, 'go', markersize=8)
        # plt.plot(x_1_up, z_1_up, 'o',  markersize=8, color='cornflowerblue')
        #
        # plt.plot(x_2_down, z_2_down, marker='o', markersize=8, color='salmon')
        # plt.plot(x_2, z_2, 'go', markersize=8)
        # plt.plot(x_2_up, z_2_up, 'bo',  markersize=8, color='cornflowerblue')
        #
        # plt.plot([0, x_max], [0, z_max], 'k--')
        # plt.plot([0, -x_max], [0, z_max], 'k--')
        # plt.xticks([])
        # plt.yticks([])
        # plt.xlabel('X [m]')
        # plt.ylabel('Z [m]')
        # plt.show()
        # plt.close()

        fig = plt.figure(1)
        ax = fig.add_subplot(1, 1, 1)

        ell_3 = Ellipse((0, 2), width=std_1 * 2, height=0.3, angle=-90, color='b', fill=False, linewidth=2.5)
        ell_4 = Ellipse((0, 2), width=std_1 * 3, height=0.3, angle=-90, color='r', fill=False,
                        linestyle='dashed', linewidth=2.5)
        ax.add_patch(ell_4)
        ax.add_patch(ell_3)
        plt.plot(0, 2, marker='o', color='skyblue', markersize=9)
        plt.plot([0, 3], [0, 4], 'k--')
        plt.plot([0, -3], [0, 4], 'k--')
        plt.xlim(-3, 3)
        plt.ylim(0, 3.5)
        plt.xticks([])
        plt.yticks([])
        plt.xlabel('X [m]')
        plt.ylabel('Z [m]')
        # plt.savefig(os.path.join('docs', fig_name))
        plt.show()
        plt.close()

    # Task error figure
    if task_error:
        plt.figure(2)
        fig_name = 'task_error.png'
        xx = np.linspace(0, 40, 100)
        mm_male = 7 / 178
        mm_female = 7 / 165
        mm_young_male = mm_male + (178-164) / 178
        mm_young_female = mm_female + (165-156) / 165
        mm_gender = gmm()
        yy_male = target_error(xx, mm_male)
        yy_female = target_error(xx, mm_female)
        yy_young_male = target_error(xx, mm_young_male)
        yy_young_female = target_error(xx, mm_young_female)
        yy_gender = target_error(xx, mm_gender)
        yy_gps = np.linspace(5., 5., xx.shape[0])
        plt.grid(linewidth=0.3)
        plt.plot(xx, yy_gps, color='y', label='GPS')
        plt.plot(xx, yy_young_male, linestyle='dotted',linewidth=2.1, color='b', label='Adult/young male')
        plt.plot(xx, yy_young_female, linestyle='dotted',linewidth=2.1, color='darkorange', label='Adult/young female')
        plt.plot(xx, yy_gender, '--', color='lightgreen', linewidth=2.8, label='Generic adult (task error)')
        plt.plot(xx, yy_female, '-.', linewidth=1.7, color='darkorange', label='Adult female')
        plt.plot(xx, yy_male, '-.', linewidth=1.7, color='b', label='Adult male')

        plt.xlim(np.min(xx), np.max(xx))
        plt.xlabel("Distance from the camera [m]")
        plt.ylabel("Localization error due to human height variation [m]")
        plt.legend(loc=(0.01, 0.55))  # Location from 0 to 1 from lower left
        # plt.savefig(os.path.join(dir_out, fig_name))
        plt.show()
        plt.close()


def target_error(xx, mm):
    return mm * xx


def gmm():
    dist_gmm, dist_men, dist_women = height_distributions()
    mu_gmm = np.mean(dist_gmm)
    mm_gmm = np.mean(np.abs(1 - mu_gmm / dist_gmm))
    mm_men = np.mean(np.abs(1 - np.mean(dist_men) / dist_men))
    mm_women = np.mean(np.abs(1 - np.mean(dist_women) / dist_women))

    print("Mean of GMM distribution: {:.4f}".format(mu_gmm))
    print("coefficient for gmm: {:.4f}".format(mm_gmm))
    print("coefficient for men: {:.4f}".format(mm_men))
    print("coefficient for women: {:.4f}".format(mm_women))


def get_confidence(xx, zz, std):

    theta = math.atan2(zz, xx)

    delta_x = std * math.cos(theta)
    delta_z = std * math.sin(theta)
    return (xx - delta_x, xx + delta_x), (zz - delta_z, zz + delta_z)


def height_distributions():

    mu_men = 178
    std_men = 7
    mu_women = 165
    std_women = 7
    dist_men = np.random.normal(mu_men, std_men, 10000000)
    dist_women = np.random.normal(mu_women, std_women, 10000000)
    dist_gmm = np.concatenate((dist_men, dist_women))
    return dist_gmm, dist_men, dist_women


def expandgrid(*itrs):
    mm = 0
    combinations = list(itertools.product(*itrs))

    for h_i, h_gt in combinations:
        mm += abs(float(1 - h_i / h_gt))

    mm /= len(combinations)

    return combinations


def plot_dist(dist_gmm, dist_men, dist_women):
    try:
        import seaborn as sns
        sns.distplot(dist_men, hist=False, rug=False, label="Men")
        sns.distplot(dist_women, hist=False, rug=False, label="Women")
        sns.distplot(dist_gmm, hist=False, rug=False, label="GMM")
        plt.xlabel("X [cm]")
        plt.ylabel("Height distributions of men and women")
        plt.legend()
        plt.show()
        plt.close()
    except ImportError:
        print("Import Seaborn first")


def get_percentile(dist_gmm):
    dd_gt = 100
    mu_gmm = np.mean(dist_gmm)
    dist_d = dd_gt * mu_gmm / dist_gmm
    perc_d, _ = np.nanpercentile(dist_d, [18.5, 81.5])  # Laplace bi => 63%
    mu_d = np.mean(dist_d)
    mm_bi = (mu_d - perc_d) / mu_d
    mad_d = np.mean(np.abs(dist_d - mu_d))

