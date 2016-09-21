
# @BEGIN GRAVITATIONAL_WAVE_DETECTION
# @IN fn_H1  @as FN_H1
# @IN fn_L1  @as FN_L1
# @PARAM fs  
# @OUT GW150914_H1_whitenbp.wav @as GW150914_H1_whitenbp.wav
# @OUT GW150914_L1_whitenbp.wav @as GW150914_L1_whitenbp.wav



# @BEGIN LOAD_DATA
# @IN fn_H1  @as FN_H1
# @IN fn_L1  @as FN_L1 
# @OUT strain_H1 @as strain_H1
# @OUT strain_L1 @as strain_L1
# @END LOAD_DATA



# @BEGIN FOURIER_DOMAIN_FILTER
# @IN strain_H1 @as strain_H1
# @IN strain_L1 @as strain_L1
# @PARAM fs  
# @OUT strain_H1_whitenbp @as strain_H1_whitenbp
# @OUT strain_L1_whitenbp @as strain_L1_whitenbp
# @END FOURIER_DOMAIN_FILTER

# @BEGIN TIME_DOMAIN_FILTER
# @IN strain_H1 @as strain_H1
# @IN strain_L1 @as strain_L1
# @PARAM fs  
# @OUT strain_H1_filt 
# @OUT strain_L1_filt 
# @END TIME_DOMAIN_FILTER



# @BEGIN WAVE_FILE_GENERATOR
# @IN strain_H1_whitenbp @as strain_H1_whitenbp
# @IN strain_L1_whitenbp @as strain_L1_whitenbp
# @OUT GW150914_H1_whitenbp.wav @as GW150914_H1_whitenbp.wav
# @OUT GW150914_L1_whitenbp.wav @as GW150914_L1_whitenbp.wav
# @END WAVE_FILE_GENERATOR


# @END GRAVITATIONAL_WAVE_DETECTION