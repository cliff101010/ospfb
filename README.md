
# OSPFB Design Files

This repository provides the CASPER hardware design files for the thesis "Design of Polyphase Filter Banks for Specific Fractional Oversampling Ratios: Implementation on an RFSoC Platform". Please refer to the thesis for the detailed architecture and derivations.

- **Platform:** Xilinx RFSoC 4x2
- **Environment:** CASPER toolflow / Ubuntu 20.04 / MATLAB R2021a / Vivado 2021.1
- **License:** GNU General Public License v2.0 (GPL-2.0)

## Abstract

In multi-stage channelization systems, the Oversampled Polyphase Filter Bank (OSPFB) effectively mitigates channel-edge scalloping loss and spectral aliasing associated with critically sampled designs. However, the data overlap introduced by oversampling necessitates an additional scheme for reusing historical samples across polyphase filter taps, and this scheme must be adjusted accordingly whenever the oversampling ratio changes, thereby increasing hardware design complexity.

To address this issue, this study constrains the oversampling ratio to satisfy $`\frac{P_{\mathrm{os}}}{D_{\mathrm{os}}} = \frac{2^k}{2^k-1}, \quad k \in \mathbb{Z}_{>0}`$ and, by analyzing the input data sequences corresponding to different oversampling ratios, derives the methods and patterns for correctly reusing historical samples across polyphase filter taps. This leads to a systematic methodology for implementing OSPFBs with integer and selected fractional oversampling ratios of 2× or less using the same design rules. Specifically, the polyphase filter is built upon existing modules; by constraining the system specifications to avoid data exchange across parallel input paths, only the inter-tap data buffering and read/write mechanisms require modification.

Based on this methodology, 2× and 4/3× OSPFBs are implemented and verified on the Xilinx RFSoC 4x2 platform. Operating at a 200 MHz system clock, the 4/3× architecture realizes a 128-channel, 8-tap channelizer with a 1200 MHz bandwidth, utilizing approximately 7% of LUTs, 8% of registers, 15% of BRAM, and 7% of DSP48 resources, while suppressing spectral image components to below -57 dB.

Furthermore, this study employs the CASPER (Collaboration for Astronomy Signal Processing and Electronics Research) toolflow to complete the entire hardware development via a graphical design approach, without writing hardware description language code or high-level synthesis C/C++ code.
