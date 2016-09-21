
# @BEGIN GRAVITATIONAL_WAVE_DETECTION
# @IN fn_H1  @as FN_H1
# @IN fn_L1  @as FN_L1
# @PARAM fs  
# @OUT GW150914_H1_whitenbp.wav 
# @OUT GW150914_L1_whitenbp.wav 
# @OUT GW150914_H1_shifted.wav 
# @OUT GW150914_L1_shifted.wav




# @BEGIN LOAD_DATA
# @IN fn_H1  @as FN_H1
# @IN fn_L1  @as FN_L1 
# @OUT strain_H1 @as strain_H1
# @OUT strain_L1 @as strain_L1
# @END LOAD_DATA




# @BEGIN AMPLITUDE_SPECTRAL_DENSITY
# @IN strain_H1 @as strain_H1
# @IN strain_L1 @as strain_L1
# @PARAM fs  
# @OUT psd_H1 @as PSD_H1
# @OUT psd_L1 @as PSD_L1
# @END AMPLITUDE_SPECTRAL_DENSITY



# @BEGIN WHITENING
# @IN psd_H1 @as PSD_H1 
# @IN psd_L1 @as PSD_L1 
# @OUT strain_H1_whiten @as strain_H1_whiten
# @OUT strain_L1_whiten @as strain_L1_whiten
# @END WHITENING



# @BEGIN BANDPASSING
# @IN strain_H1_whiten @as strain_H1_whiten
# @IN strain_L1_whiten @as strain_L1_whiten
# @OUT strain_H1_whitenbp @as strain_H1_whitenbp
# @OUT strain_L1_whitenbp @as strain_L1_whitenbp
# @END BANDPASSING


# @BEGIN FILTER_COEFS 
# @PARAM fs  
# @OUT coefs @as COEFFICIENTS
# @END FILTER_COEFS 



# @BEGIN FILTER_DATA
# @IN fn_H1 @as strain_H1 
# @IN fn_L1 @as strain_L1 
# @IN coefs @as  COEFFICIENTS
# @OUT strain_H1_filt @as strain_H1_filt
# @OUT strain_L1_filt @as strain_L1_filt
# @END FILTER_DATA



# @BEGIN SHIFT_FREQUENCY_BANDPASSED
# @IN strain_H1_whitenbp @as strain_H1_whitenbp
# @IN strain_L1_whitenbp @as strain_L1_whitenbp
# @OUT strain_H1_shifted @as strain_H1_shifted
# @OUT strain_L1_shifted @as strain_L1_shifted
# @END SHIFT_FREQUENCY_BANDPASSED

# @BEGIN GENERATE_WAVE_FILE
# @IN strain_H1_whitenbp @as strain_H1_whitenbp
# @IN strain_L1_whitenbp @as strain_L1_whitenbp
# @OUT GW150914_H1_whitenbp.wav 
# @OUT GW150914_L1_whitenbp.wav 
# @OUT GW150914_H1_shifted.wav 
# @OUT GW150914_L1_shifted.wav
# @END GENERATE_WAVE_FILE


# @END GRAVITATIONAL_WAVE_DETECTION