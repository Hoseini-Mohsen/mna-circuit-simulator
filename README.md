# MNA Circuit Simulator

A Python-based DC circuit simulator built around **Modified Nodal Analysis (MNA)**. Unlike simple series/parallel solvers, it is designed to analyze arbitrary circuit topologies rather than just series/parallel networks.

This project is a continuation of an earlier one, [DC-Circuit-Analyzer](https://github.com/Hoseini-Mohsen/DC-Circuit-Analyzer), which only handled series/parallel resistor networks. The main goal of this project is to further improve Python skills by tackling a broader, more general circuit analysis problem.

## Goals

- Support core passive and active components: resistors, capacitors, inductors, voltage sources, and current sources
- Analyze arbitrary (non-series/parallel) circuit topologies using MNA
- Extend support to dependent sources and ideal op-amps
- Define circuits via a simple JSON netlist format
- Lay the groundwork for future AC analysis alongside the current DC support

## Status

Currently in active development. The MNA core, along with resistors and independent sources under DC analysis, is implemented and tested. Dependent sources and op-amps are planned next.

## License

See [LICENSE](LICENSE).
