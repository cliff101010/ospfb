
# OSPFB Design Files

This repository provides the CASPER hardware design files for the thesis "Design of Polyphase Filter Banks for Specific Fractional Oversampling Ratios: Implementation on an RFSoC Platform". Please refer to the thesis for the detailed architecture and derivations.

- **Platform:** Xilinx RFSoC 4x2
- **Environment:** CASPER toolflow / Ubuntu 20.04 / MATLAB R2021a / Vivado 2021.1
- **License:** GNU General Public License v2.0 (GPL-2.0)

## Abstract

In multi-stage channelization systems, the Oversampled Polyphase Filter Bank (OSPFB) effectively mitigates channel-edge scalloping loss and spectral aliasing in critically sampled designs. However, data overlap from oversampling requires an additional scheme to reuse historical samples across polyphase filter taps, and adjusting this scheme whenever the oversampling ratio changes increases hardware design complexity. 

To address this issue, this study constrains the oversampling ratio to $2^k/(2^k-1)$ for a positive integer k and, by analyzing the input data sequences corresponding to different oversampling ratios, derives the methods and patterns for correctly reusing historical samples across polyphase filter taps. This leads to a systematic methodology for implementing OSPFBs with integer and selected fractional oversampling ratios of 2 or less using the same design rules. Specifically, the polyphase filter is built upon existing modules; constraining the system specifications avoids data exchange across parallel input paths, so that only the inter-tap data buffering and read/write mechanisms require modification. 

Based on this methodology, OSPFBs with ratios of 2 and 4/3 are implemented and verified on the Xilinx RFSoC 4x2 platform. At a 200 MHz system clock, the 4/3-oversampled architecture realizes a 128-channel, 8-tap channelizer with a 1200 MHz bandwidth using approximately 7% of LUTs, 8% of registers, 15% of BRAM, and 7% of DSP48 resources, suppressing spectral image components to below −57 dB. Furthermore, employing the CASPER (Collaboration for Astronomy Signal Processing and Electronics Research) toolflow, this study completes all hardware development graphically without writing hardware description language or high-level synthesis C/C++ code.
