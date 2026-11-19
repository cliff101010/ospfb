import sys, os, time, struct
from numpy import fft
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import matplotlib.animation as anim
import casperfpga
import numpy as np
import pylab
from rfsoc4x2_tut_rfdc_utils import *


def get_vacc_data_256(fpga, nchannels=8, nfft=2048):
  acc_n = fpga.read_uint('acc_cnt')
  chunk = nfft//nchannels
  print('nchannels = ', nchannels) 
  print('nfft = ', nfft)        
  print('acc_n = ', acc_n)         
  print('chunk = ', chunk)     
  raw = np.zeros((nchannels, chunk))
  for i in range(nchannels):
    raw[i,:] = struct.unpack('>{:d}Q'.format(chunk), fpga.read('q{:d}'.format((i+5)),chunk*8,0))
  print('raw = ', raw, '\n')	
  interleave_q = []
  for i in range(chunk):
    for j in range(nchannels):
      interleave_q.append(raw[j,i])
  num_channels = len(raw) 
  num_samples_per_channel = len(raw[0])  
  print('type of raw[0][0] = ', type(raw[0][0]))
  print("Number of channels:", num_channels)
  print("Number of samples per channel:", num_samples_per_channel)
  print('type(raw) = ', type(interleave_q))
  print('\n\n')
  return acc_n, np.array(interleave_q, dtype=np.float64)

def plot_spectrum_256(fpga, cx=True, num_acc_updates=None):

  fig = plt.figure(figsize=(11, 7))
  ax = fig.add_subplot(111)
  ax.grid();

  fs = 1600
  if cx:
    print('complex design')
    Nfft = 2**11
    fbins = np.arange(-Nfft//2, Nfft//2)
    nchannels = 8
    df = fs/Nfft
    faxis = fbins*df + fs/2
  else:
    print('real design')
    Nfft = 2**8   
    fbins = np.arange(0, Nfft//2)
    df = fs/Nfft
    nchannels = 4 
    faxis = fbins*df

  if cx:
    acc_n, spectrum = get_vacc_data_256(fpga, nchannels=nchannels, nfft=Nfft)
    line, = ax.plot(faxis,10*np.log10(fft.fftshift(spectrum)),'-')
  else:
    acc_n, spectrum = get_vacc_data_256(fpga, nchannels=nchannels, nfft=Nfft//2)
    line, = ax.plot(faxis,10*np.log10(spectrum),'-')

  ax.set_xlabel('Frequency (MHz)')
  ax.set_ylabel('Power (dB arb.)')

  def update(frame, *fargs):
  
    if cx:
      acc_n, spectrum = get_vacc_data_256(fpga, nchannels=nchannels, nfft=Nfft)
      line.set_ydata(10*np.log10(fft.fftshift(spectrum)))
    else:
      acc_n, spectrum = get_vacc_data_256(fpga, nchannels=nchannels, nfft=Nfft//2)
      line.set_ydata(10*np.log10(spectrum))
    print('spectrum data num = ', len(spectrum))
    print('spectrum = ', spectrum)
    current_min = np.min(10*np.log10(spectrum))
    current_max = np.max(10*np.log10(spectrum))

    if current_min < ax.get_ylim()[0] or current_max > ax.get_ylim()[1]:
            ax.set_ylim(current_min - current_min*0.05, current_max + current_max*0.1)
    
    ax.set_title('acc num: %d' % acc_n)

  v = anim.FuncAnimation(fig, update, frames=1, repeat=True, fargs=None, interval=1000)
  plt.show()



##### spec_2stage #######################
def  get_vacc_data_2stage(fpga, nchannels=8, nfft=2048):

  acc_n = fpga.read_uint('acc_cnt')
  chunk = nfft//nchannels
  print('nchannels = ', nchannels) 
  print('nfft = ', nfft)          
  print('acc_n = ', acc_n)         
  print('chunk = ', chunk)       
  raw = np.zeros((nchannels, chunk))
  for i in range(nchannels): 
    raw[i,:] = struct.unpack('>{:d}Q'.format(chunk), fpga.read('q{:d}'.format((i+1)),chunk*8,0))
  print('raw = ', raw, '\n')	
  interleave_q = []
  for i in range(chunk):
    for j in range(nchannels):
      interleave_q.append(raw[j,i])
  num_channels = len(raw)  
  num_samples_per_channel = len(raw[0])  
  print('type of raw[0][0] = ', type(raw[0][0]))
  print("Number of channels:", num_channels)
  print("Number of samples per channel:", num_samples_per_channel)
  print('type(raw) = ', type(interleave_q))
  print('\n\n')

  interleave_s = np.array(interleave_q, dtype=np.float64)
  spectrum_blocks = interleave_s.reshape((128, 512))
  spectrum_shifted_blocks = np.fft.fftshift(spectrum_blocks, axes=1)
  last_spec = np.zeros((128,256),dtype=np.float64)

  for x in range(128):
    center = 512 // 2
    selected_data = spectrum_shifted_blocks[x, center-128:center+128]
    last_spec[x, :] = selected_data
  flattened_spec = last_spec.reshape(32768, order = 'C')
  osspec_out = np.roll(flattened_spec, -128)

  return acc_n, osspec_out
  

def plot_spectrum_2stage(fpga, cx=True, num_acc_updates=None):

  fig = plt.figure(figsize=(11, 7))
  ax = fig.add_subplot(111)
  ax.grid()
  
  fs = 1600

  if cx:
    print('complex design')
    Nfft = 2**15
    fbins = np.arange(-Nfft//2, Nfft//2)
    nchannels = 4
    df = fs/Nfft
    faxis = fbins*df + fs/2
  else:
    print('real design')
    Nfft = 2**17   
    fbins = np.arange(0, Nfft//4)
    df = fs/(Nfft//2)
    nchannels = 8 
    faxis = fbins*df
    print("faxis :", faxis)
    print("freq resolution :", df)

  if cx:
    acc_n, spectrum = get_vacc_data_2stage(fpga, nchannels=nchannels, nfft=Nfft)
    line, = ax.plot(faxis,10*np.log10(fft.fftshift(spectrum)),'-')
  else:
    acc_n, spectrum = get_vacc_data_2stage(fpga, nchannels=nchannels, nfft=Nfft//2)
    line, = ax.plot(faxis,10*np.log10(spectrum),'-')

  ax.set_xlabel('Frequency (MHz)')
  ax.set_ylabel('Power (dB arb.)')

  def update(frame, *fargs):
    if cx:
      acc_n, spectrum = get_vacc_data_2stage(fpga, nchannels=nchannels, nfft=Nfft)
      line.set_ydata(10*np.log10(fft.fftshift(spectrum)))
    else:
      acc_n, spectrum = get_vacc_data_2stage(fpga, nchannels=nchannels, nfft=Nfft//2)

      line.set_ydata(10*np.log10(spectrum))
      
      # file_path = "/home/leeke/Pictures/temp/2x_spec_628_125.txt"
      # with open(file_path, "a") as f:
      #   np.savetxt(f, spectrum_db.reshape(1, -1), delimiter=",")
    
    current_min = np.min(10*np.log10(spectrum))
    current_max = np.max(10*np.log10(spectrum))
    
    max_v_index = np.argmax(spectrum)
    print("max index",max_v_index)
    min_v_index = np.argmin(spectrum)
    print("min index", min_v_index)
    max_v = np.max(spectrum)
    print("max",max_v)
    min_v = np.min(spectrum)
    print("min", min_v)
    max_freq = max_v_index * 800 / 32768

    if current_min < ax.get_ylim()[0] or current_max > ax.get_ylim()[1]:
            ax.set_ylim(current_min - current_min*0.05, current_max + current_max*0.1)
    
    # ax.set_title('acc num: %d' % acc_n)
    # for x in np.arange(0, 800 + 6.25, 6.25):
    #     ax.axvline(x=x, color='r', linestyle='--', alpha=0.25, linewidth=0.7)
    # for x in np.arange(0, fs//2 + fs/256, fs/256):
    #     ax.axvline(x=x, color='r', linestyle='--', alpha=0.25, linewidth=0.7)
    ax.text(0, 1, 'max freq: %.15f MHz' % max_freq, 
            transform=ax.transAxes, fontsize=10, 
            verticalalignment='top', horizontalalignment='left', 
            bbox=dict(facecolor='white', alpha=0.8))

  v = anim.FuncAnimation(fig, update, frames=1, repeat=True, fargs=None, interval=3000)
  plt.show()


if __name__=="__main__":
  from optparse import OptionParser

  p = OptionParser()
  p.set_usage('rfsoc4x2_tut_rfdc_plot_adc.py <HOSTNAME_or_IP> cx|real [options]')
  p.set_description(__doc__)
  p.add_option('-l', '--acc_len', dest='acc_len', type='int',default=2**31,
      help='Set the number of vectors to accumulate between dumps. default is 2*(2^28)/2048')
  p.add_option('-c', '--channel_sel', dest='adc_chan_sel', type='int',default=0,
      help='Select 0-3 ADC channel to monitor. default is channel 0.')
  p.add_option('-s', '--skip', dest='skip', action='store_true',
      help='Skip programming and begin to plot data')
  p.add_option('-b', '--fpg', dest='fpgfile',type='str', default='',
      help='Specify the fpg file to load')

  opts, args = p.parse_args(sys.argv[1:])
  if len(args) < 2:
    print('Specify a hostname or IP for your casper platform. And either cx|real to indicate the type of spectrometer design.\n'
          'Run with the -h flag to see all options.')
    exit()
  else:
    hostname = args[0]
    mode_str = args[1]
    print("mode=", mode_str)
    if mode_str=='cx':
      mode = 1
    elif mode_str=='real':
      mode = 0
    else:
      print('operation mode not recognized, must be "cx" or "real"')
      exit()

  if opts.fpgfile != '':
    bitstream = opts.fpgfile
  else:
    if mode == 1:
      fpg_prebuilt = './prebuilt/rfsoc4x2/rfsoc4x2_tut_rfdc_cx.fpg'
    else:
      fpg_prebuilt = './prebuilt/rfsoc4x2/rfsoc4x2_tut_rfdc_real.fpg'

    if opts.adc_chan_sel < 0 or opts.adc_chan_sel > 3:
      print('adc select must be 0,1,2 or3')
      exit()
    
    print('using prebuilt fpg file at %s' % fpg_prebuilt)
    bitstream = fpg_prebuilt
    
  print('Connecting to rfsoc4x2 server %s ... \n' % (hostname))
  fpga = casperfpga.CasperFpga(hostname)
  #time.sleep(0.2)

  if not opts.skip:
    print('Programming FPGA with %s...'% bitstream)
    fpga.upload_to_ram_and_program(bitstream)
    print('done')
  else:
    fpga.get_system_information()
    print('skip programming fpga...')
    
  print ('accumulation period = %d'%opts.acc_len)
  print('Configuring accumulation period...')
  fpga.write_int('acc_len', opts.acc_len)
  time.sleep(0.1)
  print('done')
    
  print("list devices = %s \n" % fpga.listdev())
  clk=fpga.estimate_fpga_clock()
  print ("\n\n\nFPGA clock = %s MHz\n\n\n"%clk)
  time.sleep(1.0)
  rfdc_rfsoc4x2 = fpga.adcs['rfdc']
  print ('RFDC = ', rfdc_rfsoc4x2)
  time.sleep(1.0)
   
  if ( rfdc_rfsoc4x2.init() == True ):
      print ("ADC init. OK \n")
      print("ADC status = %s \n"%rfdc_rfsoc4x2.status())
  else :
      print ("ADC init. failed \n")
      exit_fail()
  print ('Specify the ADC channel ...')
  
  print ('ADC channel = %d\n'%opts.adc_chan_sel)
  fpga.write_int('adc_chan_sel',opts.adc_chan_sel)
  print ('done')
  
  print('Resetting counters...')
  fpga.write_int('cnt_rst',1) 
  fpga.write_int('cnt_rst',0) 
  time.sleep(10)
  print('done')  

  try:
    # plot_spectrum_256(fpga, cx=mode)
    plot_spectrum_2stage(fpga, cx=mode)
  except KeyboardInterrupt:
    exit()
