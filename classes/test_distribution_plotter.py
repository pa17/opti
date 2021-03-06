import numpy as np
import numpy.ma as ma
from classes.model_parameters import MP
from functions.intensity_distribution import get_intensity_distr
from functions.cost import cost_obj_fun
import matplotlib.pyplot as plt
import operator as op


class PlotTestDistribution:
    """
    Two-dimensional model of light distribution in a plane with n number of light sources
    """

    def __init__(self,
                 lamp_locs = (1, 1, 1.5, 2, 3, 2.5),
                 name='',
                 refl=False,
                 save_fig=False,
                 fig_name='',
                 constrained=False,
                 cost_subsystem=False,
                 weight=-1.0):

        # These cannot be taken from the enum, as they vary upon each initialisation
        self.lamp_locs = lamp_locs
        self.name = name
        self.refl = refl
        self.save_fig = save_fig
        self.fig_name = fig_name
        self.constrained = constrained
        self.cost_subsystem = cost_subsystem
        self.weight = weight

        # Define plugs position
        self.firstplug_position = MP.F_PLUG_POSITION
        self.secondplug_position = MP.S_PLUG_POSITION

        # Plot
        if not self.cost_subsystem:
            self.plot_intensity_distr()
        else:
            self.plot_cable_distribution()

    def plot_intensity_distr(self):
        """
        Calculates the intensity distribution within a room with n number of light sources
        """

        light_intensity, minimum, minimum_coordinates = get_intensity_distr(self.lamp_locs, self.refl)

        # Fill masked areas (lamps) with maximum value
        light_intensity = ma.filled(light_intensity, np.amax(light_intensity))

        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)

        # Plot background image of room
        if not self.constrained:
            img = plt.imread("../classes/room_outline.png")
        else:
            img = plt.imread("../classes/room_outline_constr.png")

        ax.imshow(img, extent=[0, MP.ROOM_LENGTH / MP.DXY, 0, MP.ROOM_WIDTH / MP.DXY])

        # Plot intensity distribution
        ax.contourf(light_intensity, MP.N_LEVELS, cmap='plasma', alpha=0.75, antialiased=True)

        # Plot global minimum
        ax.plot(minimum_coordinates[1], minimum_coordinates[0], 'ro', markersize=12)

        # Layout & Titles
        plt.suptitle(self.name + " Optimisation", fontweight='bold')

        plt.title("Reflections: " + str(self.refl) + ", Constraints: " + str(self.constrained)
                  + ", Minimum: " + str(round(minimum, 2)), fontsize='large')

        plt.xlabel('Room X-Position (cm)')
        plt.ylabel('Room Y-Position (cm)')

        # Export figure
        if self.save_fig:
            plt.savefig(self.fig_name + str(self.refl) + str(self.constrained) + '.svg', format='svg', dpi=1200)

        # Show figure

        plt.show()

    def plot_cable_distribution(self):
        """
               Calculate the position of the cables
               Also plot the the intensity distribution within a room with n number of light sources
               The later one is obtained from the light subsystem
               """

        light_intensity, minimum, minimum_coordinates = get_intensity_distr(self.lamp_locs, self.refl)

        total_cost = cost_obj_fun(self.lamp_locs)

        # Fill masked areas (lamps) with maximum value
        light_intensity = ma.filled(light_intensity, np.amax(light_intensity))

        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)

        # Plot background image of room
        if not self.constrained:
            img = plt.imread("../classes/room_outline.png")
        else:
            img = plt.imread("../classes/room_outline_constr.png")

        ax.imshow(img, extent=[0, MP.ROOM_LENGTH / MP.DXY, 0, MP.ROOM_WIDTH / MP.DXY])

        # Plot intensity distribution
        ax.contourf(light_intensity, MP.N_LEVELS, cmap='plasma', alpha=0.75, antialiased=True)

        # Plot global minimum
        ax.plot(minimum_coordinates[1], minimum_coordinates[0], 'ro', markersize=12)


        #Plot cost
        for i in range(MP.N_LAMPS):

            lamp_position = [self.lamp_locs[2 * i], self.lamp_locs[2 * i + 1]]
            # Distance to first plug and second plug
            d_fp = list(map(op.sub, lamp_position, self.firstplug_position))
            d_sp = list(map(op.sub, lamp_position, self.secondplug_position))

            # Therefore cable length for L shape
            l_fp = (abs(d_fp[0]) + abs(d_fp[1]))
            l_sp = (abs(d_sp[0]) + abs(d_sp[1]))


            #Connect lamp cable to nearest plug

            if l_fp <= l_sp:
                plt.plot([100 * self.firstplug_position[0], 100 * self.lamp_locs[2 * i]],
                         [100 * self.firstplug_position[1], 100 * self.firstplug_position[1]], "grey")
                plt.plot([100 * self.lamp_locs[2 * i], 100 * self.lamp_locs[2 * i]],
                         [100 * self.firstplug_position[1], 100 * self.lamp_locs[2 * i + 1]], "grey")
            else:
                plt.plot([100 * self.secondplug_position[0], 100 * self.lamp_locs[2 * i]],
                         [100 * self.secondplug_position[1], 100 * self.secondplug_position[1]], "grey")
                plt.plot([100 * self.lamp_locs[2 * i], 100 * self.lamp_locs[2 * i]],
                         [100 * self.secondplug_position[1], 100 * self.lamp_locs[2 * i + 1]], "grey")


        # Layout & Titles
        plt.suptitle(self.name + " Optimisation", fontweight='bold')

        if self.weight <= 0.0:
            plt.title("Constraints: " + str(self.constrained) + ", Minimum: " + str(round(minimum, 2)) +
                      ", Cost: " + str(round(total_cost, 2)), fontsize='large')
        else:
            plt.title("Constraints: " + str(self.constrained) + ", Minimum: " + str(round(minimum, 2)) +
                      ", Cost: " + str(round(total_cost, 2)) + " Weight (Light): " + str(self.weight), fontsize='large')

        plt.xlabel('Room X-Position (cm)')
        plt.ylabel('Room Y-Position (cm)')
        # Export figure
        if self.save_fig:
            plt.savefig('../plots/' + self.fig_name + str(self.refl) + str(self.constrained) + str(self.cost_subsystem) + 
            	'.svg', format='svg', dpi=1200)

        # Show figure
        plt.show()



if __name__ == '__main__':

    PlotTestDistribution([1.19861974, 0.96961294, 1.6086077 , 1.98102811, 3.67479242, 1.18626474, 0.26990641],
                         'Trust-Constr', True, True, 'Sys_lvl', True, True, 1.0)
