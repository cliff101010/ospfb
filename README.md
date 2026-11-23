# OSPFB Design Files

This repository provides the CASPER hardware design files for the thesis "Design of Polyphase Filter Banks for Specific Fractional Oversampling Ratios: Implementation on an RFSoC Platform". Please refer to the thesis for the detailed architecture and derivations.

- **Platform:** Xilinx RFSoC 4x2
- **Environment:** CASPER toolflow / Ubuntu 20.04 / MATLAB R2021a / Vivado 2021.1
- **License:** GNU General Public License v2.0 (GPL-2.0)

## Abstract

In multi-stage channelization systems, the Oversampled Polyphase Filter Bank (OSPFB) effectively mitigates scalloping loss at channel edges and spectral aliasing inherent in critically sampled designs. However, the data overlap introduced by oversampling necessitates an additional scheme for reusing historical samples across polyphase filter taps, and this scheme must be adjusted accordingly whenever the oversampling ratio changes, thereby increasing hardware design complexity.

To address this issue, this study constrains the selection of oversampling ratios so that the oversampled hardware architecture can be designed under a unified set of rules. By analyzing the input data sequences under different oversampling ratios, the methods and patterns for accurately reusing historical samples across taps are derived, establishing a systematic methodology capable of implementing both integer and specific fractional OSPFB with the same design rules. Specifically, the polyphase filter is built upon existing modules; by constraining the system specifications to avoid data exchange across parallel input paths, only the inter-tap data buffering and read/write mechanisms require modification.

Based on this methodology, 2× and 4/3× OSPFBs are implemented and verified on the Xilinx RFSoC 4x2 platform. Operating at a 200 MHz system clock, the 4/3× architecture realizes a 128-channel, 8-tap channelizer with a 1200 MHz bandwidth, utilizing approximately 7% of LUTs, 8% of registers, 15% of BRAM, and 7% of DSP48 resources, while suppressing spectral image components below -57 dB.

Furthermore, this study employs the CASPER (Collaboration for Astronomy Signal Processing and Electronics Research) toolflow to complete the entire hardware development via a graphical design approach, without writing Hardware Description Language or High-Level Synthesis C/C++ code.
