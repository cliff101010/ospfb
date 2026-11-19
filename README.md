# OSPFB Design Files

This repository provides the CASPER hardware design files for the thesis "Design of Polyphase Filter Banks for Specific Fractional Oversampling Ratios: Implementation on an RFSoC Platform". Please refer to the thesis for the detailed architecture and derivations.

- **Platform:** Xilinx RFSoC 4x2
- **Environment:** CASPER toolflow / Ubuntu 20.04 / MATLAB R2021a / Vivado 2021.1
- **License:** GNU General Public License v2.0 (GPL-2.0)

## Abstract

Oversampled polyphase filter banks (OSPFBs) in multi-stage channelization systems effectively mitigate channel-edge scalloping loss and spectral aliasing in critically sampled designs. However, oversampling introduces data overlap requiring extra inter-tap historical-sample reuse; adapting it for different oversampling ratios increases hardware complexity.

To address this issue, this study restricts oversampling-ratio selection to unify hardware design rules and analyzes input sequences across oversampling ratios to identify accurate inter-tap historical-sample reuse patterns, establishing a unified methodology for integer and specific fractional OSPFBs. With the polyphase filter built on existing modules, system specification constraints avoid data exchange across parallel input paths, requiring only inter-tap buffering and read/write adjustments.

Using this methodology, 2× and 4/3× OSPFBs are implemented and verified on the Xilinx RFSoC 4x2 platform. At a 200 MHz system clock, the 4/3× architecture realizes a 128-channel, 8-tap channelizer with 1200 MHz bandwidth, using about 7% LUTs, 8% registers, 15% BRAM, and 7% DSP48 resources while suppressing spectral images below -57 dB.

Moreover, hardware is developed entirely graphically via the CASPER (Collaboration for Astronomy Signal Processing and Electronics Research) toolflow without writing Hardware Description Language or High-Level Synthesis C/C++ code.
