# UNS Innovation Hackathon 2026

Archive of the Aethera team's work for the UNS Innovation Hackathon 2026 (Hackathon Deeptech program). The project is WattLink, a plug-and-play wireless sub-metering system with edge AI. It measures the energy use of single machines in small businesses (UMKM) and public facilities, and it can cut the power to a machine that overloads.

This repository is a read-only record. The running product lives in the repositories of the `aethera-deeptech` organization.

## Related repositories

| Repository | Content |
|---|---|
| [aethera-deeptech/firmware](https://github.com/aethera-deeptech/firmware) | Firmware of the hub and the sensor nodes |
| [aethera-deeptech/backend](https://github.com/aethera-deeptech/backend) | API of the energy audit dashboard |
| [aethera-deeptech/frontend](https://github.com/aethera-deeptech/frontend) | Web dashboard |
| [aethera-deeptech/demo-seeder](https://github.com/aethera-deeptech/demo-seeder) | Keeps the demo accounts of the backend alive with simulated gateways |

## How the prototype works

- Sensor nodes (a Plug and a Clamp) use an ESP32-C3 with a PZEM-004T meter. They send telemetry to the hub over ESP-NOW and receive relay commands back.
- The hub is an ESP32 DevKit V1 with a 0.96 inch OLED. It forwards the data over Wi-Fi to the backend.
- The web dashboard shows usage per device and sends cut-off commands.

## Layout

| Folder | Content |
|---|---|
| `docs/organizer` | Guidebook and briefing slides of the hackathon organizer |
| `docs/team` | Prototype document and the device design (`Aethera_Rancangan Alat.pdf`) |
| `hardware/enclosures` | 3D enclosures of the Hub, Plug, Clamp and Clamp meter. STL and STEP files, renders, `assumptions.md` and `checks.md` |
| `hardware/models` | Third-party STEP models used in the enclosures. `SOURCES.txt` lists where each one came from |
| `firmware/hub`, `firmware/plug` | MicroPython test and demo scripts, the MicroPython images for the boards, and a prebuilt hub build in `firmware/hub` |
| `firmware/hub-flash-*` | Prebuilt hub firmware. `5ad43d1` is [PR 58](https://github.com/aethera-deeptech/firmware/pull/58) and `a58a75e` is [PR 57](https://github.com/aethera-deeptech/firmware/pull/57) of the firmware repository |
| `documentation/diagrams` | Architecture and schematic diagrams |
| `documentation/test-photos` | Photos of the assembled prototype |
| `documentation/dashboard` | Screenshots of the dashboard |
| `documentation/demo-video` | Two camera angles of the ESP-NOW relay demo |

## Not included

Personal and administrative documents of the team (identity cards, signatures, CVs, certificates and the signed proposal forms) are not part of this archive.

## Rights

No license is granted for the original work in this repository, so all rights are reserved by the authors.

The organizer documents and the third-party 3D models belong to their own authors and owners. They are kept here as reference material only. Check `hardware/models/SOURCES.txt` and the originals before you reuse them.
