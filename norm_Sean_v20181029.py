#==============Normalization of the quasar spectra=================
# THIS FILE:
# Imports the neccessary libraries
# Specify the range of spectra list(if needed)
# Reads data from .csv files and assign to the three different lists
# Uses the powerlaw and calculates the normalization of spectra with given SDSS data
# Plots the necessary values to the graph (as figures)
# Saves these figures to the pdf spectrum files. (Given location)
# At the end saves


# ====================================================================



#============Import Files and Libraries========================
import os
import numpy as np 
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.backends.backend_pdf import PdfPages
import utility_functions
#================================================================

def normalize_spectra():
    #===========Specifying The Range==============================
    # this is a range that how many spectra you want to check
    # and/or between spectras in the file
    starts_from = 0
    ends_at = 9
    good_categorized_spectra_list = range(starts_from, ends_at)

    #For IDE run, locate the file
    config_file = "sorted_norm.csv" 

    #For command line, activate this config_file
    #config_file = sys.argv[1] 
    #================================================================

    #============Set location of spectrum files========================
    specdirec = os.getcwd() + "/files/"
    pp1 = PdfPages('original_all_graph_Sean.pdf') 
    pp2 = PdfPages('normalized_all_graph_Sean.pdf')  
    #================================================================

    log_file = "log.txt"
    utility_functions.clear_file(log_file)

    # number_of_spectra = 6760
    number_of_spectra = utility_functions.file_length(config_file)


    spectra_list = list()
    redshift_value_list = list()
    snr_value_list = list()


    #========Reading the file and assignin to the specific lists============
    with open(config_file) as f:
        for line in f:
            each_row_in_file = line.split(",")
            spectra_list.append(each_row_in_file[0])
            redshift_value_list.append(np.float(each_row_in_file[1]))
            snr_value_list.append(np.float(each_row_in_file[2]))
    #============End of Reading and Assigning=============================== 


    b = 1250 #powerlaw
    c = -0.5 #powerlaw
    counter = 0
    count_fig1 = 0
    count_fig2 = 2 * number_of_spectra # count_fig2 will always start counting from twice the number of total spectra

    ee = []
    processed_spectra_file_names = []
    eee = []

    init_pars = [b, c]

    powerlaw_not_made = []

    #==================POWERLAW FUNCTION==============================
    # Powerlaw function takes 3 parameters. Parameters b and c are defined above.
    # The parameter x is calculation of wavelength. The powerlaw calculates a value
    # as in formula and return a floating value. 
    def powerlaw(x, b, c):
        return b * (np.power(x, c))
    #==================END OF POWERLAW FUNCTION=========================
        

    ################################################################################
    ################################################################################
    ###########THIS HUGE FOR LOOP STARTS HERE AND FINISHES AROUND LINE 450s ########

    for index in good_categorized_spectra_list:
        counter += 1
    
        current_spectrum_file_name = spectra_list[index]
        
        z = round(redshift_value_list[index], 5)
        snr = round(snr_value_list[index], 5)

        print(str(counter) + ": " + current_spectrum_file_name)
        utility_functions.print_to_file(str(counter) + ": " + current_spectrum_file_name, log_file)

        
        data = np.loadtxt(specdirec + current_spectrum_file_name) 

        # Only calculating spectrum from 1200 - 1800 rest frame wavelength
        wavelength_emit1_initial = 1200
        wavelength_emit2_initial = 1800
        

        wavelength_observe1 = (z+1)*wavelength_emit1_initial
        wavelength_observe2 = (z+1)*wavelength_emit2_initial
        
        wavelength_NV_emit = 1242.8040
        # Shift Nitrogen V (NV) line into frame
        wavelength_NV_obs = (z+1)*wavelength_NV_emit

        wavelength_restframe_starting_point = 1280.206
        wavelength_restframe_ending_point = 1284.333
        
        wavelength_observed_starting_point = (z+1)*(wavelength_restframe_starting_point)
        wavelength_observed_ending_point = (z+1)*(wavelength_restframe_ending_point)

        # a good range of rest frame wavelength is = 1686 - 1773
        # their midpoint is 1729, so im gonna take 1686-1729, average them up, and find the midpoint,
        # then find midpoint of 1729-1773
        wavelength_new_emit1 = 1282.398  # 1st point for powerlaw, Point C
        
        wavelength_new_obs1 = (z+1)*wavelength_new_emit1
        
        # FIRST POINT
        # Get all points from data with wavelengths less than our starting wavelength for our first point
        q6 = np.where(data[:, 0] < wavelength_observed_starting_point)

        p7 = 0
        try:  
            p7 = np.max(q6)
        except:
            pass

        q8 = np.where(data[:, 0] > wavelength_observed_ending_point)
        
        p9 = np.min(q8)

        flux3 = data[p7:p9, 1]  
    
        median_flux3 = np.median(flux3)
        
        wavelength_flux3 = data[p7:p9, 0]
        
        median_wavelength3 = np.median(wavelength_flux3)
        
        first_point = (median_wavelength3, median_flux3)

        print(flux3)
        utility_functions.print_to_file(flux3, log_file)

        wavelength_new_emit2 = 1677.938  # Point B
        wavelength_new_emit3 = 1725.669  # Point A
        
        wavelength_new_midpoint = (wavelength_new_emit2 + wavelength_new_emit3)/2

        wavelength_new_obs2 = (z+1)*wavelength_new_emit2  # Shift point 2
        wavelength_new_obs3 = (z+1)*wavelength_new_emit3  # Shift point 3
        wavelength_new_midpoint_obs = (z+1)*wavelength_new_midpoint  # Shift midpoint

        ######################### MIDDLE POINT ##################################
        q1 = np.where(data[:, 0] < wavelength_new_obs2)  
        p1 = np.max(q1)
        q2 = np.where(data[:, 0] > wavelength_new_midpoint_obs)
        p2 = np.min(q2)

        flux1 = data[p1:p2, 1]
    
        median_flux1 = np.median(flux1)  
        wavelength_flux1 = data[p1:p2, 0]  
        
        median_wavelength1 = np.median(wavelength_flux1)
        middle_point = (median_flux1, median_wavelength1)
        ########################### END OF MIDDLE POINT ##############################
        
        
        ########################### LAST POINT###################################
        
        q3 = np.where(data[:, 0] < wavelength_new_midpoint_obs)
        p3 = np.max(q3)

        q4 = np.where(data[:, 0] > wavelength_new_obs3)
        p4 = np.min(q4)

        flux2 = data[p3:p4, 1]

        median_flux2 = np.median(flux2) 
        wavelength_flux2 = data[p3:p4, 0] 

        median_wavelength2 = np.median(wavelength_flux2)
        last_point = (median_flux2, median_wavelength2)
        
        ########################### END OF LAST POINT ##############################
        
        
    
        ######################## D POINT AND THREE POINTS #######################
        # range taken in rest frame: 1415-1430
        dpoint_starting_point_restframe = 1415 # Point D
        dpoint_ending_point_restframe = 1430 # Point D


        dpoint_starting_point = (z+1)*(dpoint_starting_point_restframe)
        dpoint_ending_point = (z+1)*(dpoint_ending_point_restframe)

    
        qq6 = np.where(data[:, 0] < dpoint_starting_point)
        try:
            pp7 = np.max(qq6)
        except:
            pass

        qq8 = np.where(data[:, 0] > dpoint_ending_point)
        pp9 = np.min(qq8)

        flux33 = data[pp7:pp9, 1]  
    
        median_flux33 = np.median(flux33)  
        wavelength_flux33 = data[pp7:pp9, 0]   
        median_wavelength33 = np.median(wavelength_flux33)
    
        dpoint = (median_wavelength33, median_flux33)

        # AVERAGE ERROR FOR D POINT
        error33 = data[pp7:pp9, 2]
        
        median_flux_error33 = np.median(error33)  
        st_dev_of_flux = np.std(flux33[:]) #Standart deviation of flux
    
        dpoint_error = (median_wavelength33, median_flux_error33)

        # THE THREE POINTS (THE THREE POINTS THAT THE original power law WILL USE)
        power_law_datax = (median_wavelength3, median_wavelength1, median_wavelength2)
        power_law_datay = (median_flux3, median_flux1, median_flux2)

        # THE THREE POINTS (THE THREE POINTS THAT THE second power law WILL USE)
        power_law_datax2 = (median_wavelength33, median_wavelength1, median_wavelength2)
        power_law_datay2 = (median_flux33, median_flux1, median_flux2)

        ############# END OF D POINT AND THREE POINTS #################################
        
        
        

        # BASICALLY, DEFINING MY WAVELENGTH, FLUX, AND ERROR (OR CHOOSING THEIR RANGE)
        wavelength_lower_limit = np.where(data[:, 0] > wavelength_observe1)
        wavelength_upper_limit = np.where(data[:, 0] < wavelength_observe2)
        

        wavelength = data[np.min(wavelength_lower_limit[0])
                                : np.max(wavelength_upper_limit[0]), 0]
        actual_wavelength = wavelength
        
        flux = data[np.min(wavelength_lower_limit[0]): np.max(
            wavelength_upper_limit[0]), 1] 
        
        
        error = data[np.min(wavelength_lower_limit[0]): np.max(
            wavelength_upper_limit[0]), 2]
        
        messed_up_error = np.where(data[np.min(wavelength_lower_limit[0]): np.max(
            wavelength_upper_limit[0]), 2] > 3) 

        wavelength_emit = wavelength/(z+1)


        fev = 10000

        print(power_law_datax)
        utility_functions.print_to_file(power_law_datax, log_file)
        print(power_law_datay)
        utility_functions.print_to_file(power_law_datay, log_file)

        # CURVE FIT FOR FIRST POWERLAW
        try:
            pars, covar = curve_fit(powerlaw, power_law_datax,
                                    power_law_datay, p0=init_pars, maxfev=fev)
        except:
            print("Error - curve_fit failed-1st powerlaw " + current_spectrum_file_name)
            utility_functions.print_to_file("Error - curve_fit failed-1st powerlaw " + current_spectrum_file_name, log_file)
            powerlaw_not_made.append(current_spectrum_file_name)

        normalizing = flux/powerlaw(wavelength, *pars)
        error_normalized = error/powerlaw(wavelength, *pars)
    
            
        for n in range(1, len(normalizing)-5):
            
            if abs(normalizing[n + 1] - normalizing[n]) > 0.5:

                if error_normalized[n+1] > 0.25:
                    error_normalized[n+1] = error_normalized[n]
                    normalizing[n+1] = normalizing[n]  # normalized graph
                    error[n+1] = error[n]  # original error
                    flux[n+1] = flux[n]  # original graph

            if error_normalized[n] > 0.5:
                error_normalized[n] = error_normalized[n-1]
                normalizing[n] = normalizing[n-1]  # normalized graph
                error[n] = error[n-1]  # original error
                flux[n] = flux[n-1]  # original graph


            if abs(normalizing[n + 1] - normalizing[n]) > 5:
                
                error_normalized[n+1] = error_normalized[n]
                normalizing[n+1] = normalizing[n]  # normalized graph
                error[n+1] = error[n]  # original error
                flux[n+1] = flux[n]  # original graph

   
        bf = pars[0]
        cf = pars[1]

        # REQUIREMENT FOR USING #POWERLAW.
        if (bf)*(np.power(median_wavelength33, cf)) > (median_flux33) - (3)*(median_flux_error33):

            ee.append(pars[0])
            eee.append(pars[1])
            processed_spectra_file_names.append(current_spectrum_file_name)
            print("processed_spectra_file_names below: ")
            print(processed_spectra_file_names)

        # SNR Calculations:

        less_than_SNR = np.where (wavelength/(z+1.) < 1250.)
        greater_than_SNR = np.where (wavelength/(z+1.) > 1400.)
        
        snr_12001600mean = []
        snr_12001600median = []
        snr_1700 = []
        
    
        if len(less_than_SNR[0]) > 0:
            
            mean_error = np.mean(1./error_normalized[np.max(less_than_SNR[0]):np.min(greater_than_SNR)])
            snr_12001600mean.append(round(mean_error,5))
            
            
            median_error = np.median(1./error_normalized[np.max(less_than_SNR[0]):np.min(greater_than_SNR)])
            snr_12001600median.append(round(median_error,5))
            
            snr_1700.append(snr)


        # Start of Figure 1
            
        plt.figure(count_fig1)


        # IF STATEMENT IS THERE TO AVOID ANY RANDOM, WEIRD PIXEL PROBLEM WITH THE ERRORS. FOR EXAMPLE: TO AVOID CASES WHERE THE ERROR IS 100
        
        if (bf)*(np.power(median_wavelength33, cf)) < (median_flux33) - (3)*(median_flux_error33):
            
            
            plt.plot(wavelength, powerlaw(wavelength, *pars), 'r--')
            plt.plot(median_wavelength33, median_flux33 - median_flux_error33, 'yo')
            plt.plot(median_wavelength33, median_flux33 -
                3*(median_flux_error33), 'yo')
            plt.plot(median_wavelength3, median_flux3, 'yo')
            plt.plot(median_wavelength33, median_flux33 - st_dev_of_flux, 'go')
            plt.title(current_spectrum_file_name)
            plt.xlabel("Wavelength[A]")
            plt.ylabel("Flux[10^[-17]]cgs")
            plt.text(((wavelength_observe1+wavelength_observe2)/2.17), np.max(flux),"z = " + str(z) + " snr=" + str(snr)+ " snr_1326=" +str(snr_12001600mean[0]) , style = 'italic')
            plt.plot(median_wavelength33, median_flux33, 'yo')
            plt.plot(wavelength, flux, 'b-')
            plt.plot(power_law_datax2, power_law_datay2, 'ro')
            plt.plot(wavelength, error, 'k-')
            
        else:

            plt.plot(wavelength, powerlaw(wavelength, *pars), 'r--')
            plt.plot(median_wavelength33, median_flux33 - median_flux_error33, 'yo')
            plt.plot(median_wavelength33, median_flux33 -
                3*(median_flux_error33), 'yo')
            plt.plot(median_wavelength33, median_flux33 - st_dev_of_flux, 'go')
            plt.title(current_spectrum_file_name)
            plt.xlabel("Wavelength[A]")
            plt.ylabel("Flux[10^[-17]]cgs")
            plt.text(((wavelength_observe1+wavelength_observe2)/2.17),np.max(flux), "z = " + str(z) + " snr=" + str(snr)+ " snr_1325=" + str(snr_12001600mean[0]))
            #plt.text(wavelength_observe1 + 1000, np.max(flux)-10, current_spectrum_file_name)
            plt.plot(median_wavelength33, median_flux33, 'yo')
            plt.plot(wavelength, flux, 'b-')
            plt.plot(power_law_datax, power_law_datay, 'ro')
            plt.plot(wavelength, error, 'k-')


        pp1.savefig()
        plt.close(count_fig1)
        # End of Figure 1
        
        
        # Start of Figure 2
        plt.figure(count_fig2)
        0.2, "z=" + str(z) + " snr=" + str(snr)

        plt.text(wavelength_observe1 + 1000, np.max(normalizing)-0.2, current_spectrum_file_name)
        plt.title(current_spectrum_file_name)
        n1 = np.where(normalizing < 1)
        n2 = wavelength[n1] 
        n3 = normalizing[n1] 
        
        plt.plot(wavelength, normalizing,'b-')#I CHANGED THIS JUST NOW
        plt.plot((wavelength[0], wavelength[-1]),(1, 1),'r-')
        #plot((wavelength[0], wavelength[-1]),(1, 1))
        plt.plot(wavelength, error_normalized,'k-') #I CHANGED THIS JUST NOW
        plt.title("normalized data vs. normalized error")
        plt.xlabel("Normalized Wavelength [A]")
        plt.ylabel("Flux[10^[-17]]cgs")
        pp2.savefig()
        plt.close(count_fig2)

        
        # End of Figure 2
        
        www = (wavelength, normalizing, error_normalized)
        www = (np.transpose(www))
        oo=current_spectrum_file_name[0:20]
        
        #########################################################################################
        # This is where normalized files will be saved. Remember to change to your own directory!
        
        np.savetxt(specdirec + oo +'norm.dr9', www)  # ,fmt='%s')
        #########################################################################################
        count_fig1 = count_fig1+1
        count_fig2 = count_fig2+1


    ############### THE FOR LOOP STARTED AT LINE ~95 FINISHED HERE #####################
    #####################################################################################
    #####################################################################################

    # EVERYTHING BELOW IS NOT IN THE FOR LOOP

    final_initial_parameters = [processed_spectra_file_names, ee, eee]
    final_initial_parameters = (np.transpose(final_initial_parameters))

    # processed_spectra_file_names is the list of all good spectra.

    for l in powerlaw_not_made:
        for lj in processed_spectra_file_names:
            if lj in powerlaw_not_made:
                processed_spectra_file_names.remove(lj)
        
            
    pp1.close()
    pp2.close()


    np.savetxt(specdirec + "/Final_Initial_Parameters.txt", final_initial_parameters, fmt="%s")
    np.savetxt(specdirec + "/good_spectra.txt", processed_spectra_file_names, fmt='%s')
    np.savetxt(specdirec + "/Powerlaw1_did_not_work.txt", powerlaw_not_made, fmt='%s')


def main():
    normalize_spectra()

if __name__ == "__main__":
    main()