# Otto DIY — evidence and cost notes

Checked 2026-10-26. Status: research complete; no software or hardware implementation, purchase, or physical verification.

## Identity and reusable assets

- The user-linked [Open-Hardware-Leaders/OttoDIY](https://github.com/Open-Hardware-Leaders/OttoDIY) is a useful older source snapshot, with 4 SG90 9 g PWM servos, Nano ATmega328, Nano I/O shield, HC-SR04, buzzer, 4-AA supply, printed body/head/legs/feet, and assembly manuals. It should not be represented as the newest maintained firmware.
- Its [CAD folder](https://github.com/Open-Hardware-Leaders/OttoDIY/tree/master/CAD) contains OpenSCAD, FreeCAD, Fusion archive and STEP sources. The repository also has STL files and [manuals](https://github.com/Open-Hardware-Leaders/OttoDIY/tree/master/How%20to%20guides). This makes changing the outer shell practical while retaining joint axes and mounting interfaces.
- [Official current library](https://github.com/OttoDIY/OttoDIYLib): GPL-3.0 LICENSE; README labels Otto design resources CC-BY-SA-4.0. README says mainly Nano, ESP32 support “in development.” Do not promise drop-in ESP32 compatibility.
- [Header](https://raw.githubusercontent.com/OttoDIY/OttoDIYLib/main/src/Otto.h) exposes walk, turn, home, bend, swing, gesture and trim functions. [Implementation](https://raw.githubusercontent.com/OttoDIY/OttoDIYLib/main/src/Otto.cpp) uses programmed servo oscillations, not learned RL policies. Blocking movement loops mean a responsive stop/watchdog API needs adaptation or bounded short commands; merely wrapping walk in a network API is insufficient.
- [Official site](https://www.ottodiy.com/) distinguishes classic Otto DIY from newer HP Otto. `https://github.com/OttoDIY/OttoDIY` currently redirects to OttoNinja; do not mix its BOM with classic 4-servo Otto.

## Mechanical interpretation and limits (engineering assessment)

Otto is a little box-headed biped with two broad feet and 4 actuated axes, two per leg, no actuated knees. It waddles using body sway and foot rotation, turns and dances on suitable flat surfaces. It is a low-cost movement/interaction demonstrator, not a substitute for a dynamically balancing 10–14-axis biped. A lightweight custom shell is reasonable; heavier camera/computer/battery hardware changes center of mass and needs gait testing. Do not assume an unmodified original body can carry a Pi plus a large power bank.

The checked official library/repositories do not provide a verified ready-to-run MuJoCo/Webots model, pretrained RL policy, or sim-to-real pipeline. This is a bounded finding, not proof none exists in the wider community. CAD can be used to build a simulator model, but joints, masses, inertias, friction, motor limits, backlash and control timing must be added. Reusing its programmed gait is easier than starting RL.

## Verified price anchors (USD, before shipping/tax)

| Part | Price | Source / use |
|---|---:|---|
| Original Arduino Nano A000005 | 25.70 | [Arduino US store](https://store-usa.arduino.cc/products/arduino-nano) — conservative choice for existing Otto library |
| TowerPro SG92R micro servo | 5.95 each | [Adafruit 169](https://www.adafruit.com/product/169) — useful priced 9 g PWM alternative; check mounting/horn differences against SG90 CAD |
| 5 V 4 A bench adapter | 14.95 | [Adafruit 1466](https://www.adafruit.com/product/1466) — test stand, separate servo power wiring |
| HC-SR04 ultrasonic module | 3.95 | [Adafruit 3942](https://www.adafruit.com/product/3942) — compatible with 5 V Nano; 3.3 V MCU inputs require level adjustment |
| Raspberry Pi Zero 2 W | 19.05 retail | [Adafruit 5291](https://www.adafruit.com/product/5291); manufacturer [MSRP 15](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) is different |
| Raspberry Pi Camera Module 3 Standard | 29.25 | [Adafruit 5657](https://www.adafruit.com/product/5657) |
| Zero FPC camera cable | 3.95 | Listed accessory on same Camera 3 page; required, ordinary camera cable does not fit Zero |
| SPH0645LM4H I2S microphone | 6.95 | [Adafruit 3421](https://www.adafruit.com/product/3421) |
| MAX98357A I2S amplifier | 5.95 | [Adafruit amplifier catalog](https://www.adafruit.com/category/526); add a small speaker, estimated 3–5 |
| XIAO ESP32S3 Sense | 13.99 | [Seeed manufacturer store](https://www.seeedstudio.com/XIAO-ESP32S3-Sense-p-5639.html) — MCU + Wi-Fi + camera + microphone |

SG90 original manufacturer [datasheet page](https://towerpro.com.tw/product/sg90-7/) has no verified unit price. It states 9 g, 1.8 kg·cm stall at 4.8 V. Stall torque is not continuous usable torque. Do not assert a generic SG90 clone is identical or that 180° rotation is guaranteed. Old Otto blog kit prices 29.99/49.99 are historical, not a confirmed current checkout offer.

## Proposed first stand and arithmetic

Conservative Nano path, reusing stock library later:

- Nano 25.70 + two SG92R at 11.90 + 5 V 4 A adapter 14.95 + wiring/USB/connector/printed test bracket allowance 10–20 = **62.55–72.55**, rounded **65–75**.
- With one servo: **56.60–66.60**. Existing suitable board or supply lowers actual incremental expense.
- Servos powered from the external regulated rail with common ground; do not draw motor current through an MCU GPIO or the Nano regulator. This is a fixed test stand, not a walking robot.

Lowest cost camera-first alternative, clearly a custom integration:

- XIAO ESP32S3 Sense 13.99 + two servos 11.90 + adapter 14.95 + wiring/bracket 10–20 = **50.84–60.84**, rounded **50–65**.
- Wi-Fi camera and microphone included; need adapt/test ESP32Servo, Otto gait timing and command processing. [Seeed wiki](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/) provides webcam examples; contemporary board lots may have OV3660 or OV5640, not necessarily the old OV2640. On battery power its 5 V pin has no voltage; a separate servo power stage is necessary. This is a good alternative to placing a Pi on a very small Otto.

## Full assembly planning estimates (not a verified final basket)

Costs below include mobile power allowance and printed mechanical parts; they exclude shipping, taxes, tools, 3D printer, external computer/AI API and optional IMU. Supply and battery selection must be finalized against mass and current constraints.

Classic autonomous Otto with Nano: Nano 25.70 + 4×5.95 servos 23.80 + HC-SR04 3.95 + buzzer 1.50 estimated + print/fasteners 12–25 + wiring 10–15 + AA holder/rechargeables/charger 20–35 = **96.95–129.95**, about **100–130**. Shield is not required if wired directly; if used, add separately. The cheaper $50–80 class is plausible with generic clone electronics, but not supported here by verified exact current offers.

Compact external-AI Otto using XIAO Sense: controller/camera/mic 13.99 + servos 23.80 + HC-SR04 3.95 + amplifier/speaker 9.95 estimated + print 12–25 + wiring 10–15 + battery/regulation/charging allowance 25–40 = **99.69–132.69**, plan **100–150**. This needs custom electrical integration and firmware; do not call it a tested kit.

Nano + Pi Zero 2 W + Camera 3 variant: Nano 25.70 + servos 23.80 + HC-SR04 3.95 + Pi 19.05 + Camera 29.25 + FPC 3.95 + microSD 8 estimated + USB connection 5 estimated + audio 17.85 estimated + mechanics 12–25 + wiring 10–15 + mobile power 30–50 = **188.55–226.55**, plan **190–250**. Extra mass and packaging make this less attractive than XIAO for original Otto proportions; it needs actual load verification.

Recommendation: Otto is the most economical way to learn actuator control, custom 3D parts and a camera-to-AI-to-action loop. If the final goal is Microduck-style locomotion, these PWM servos and gait code are primarily educational, not a directly scalable actuator/policy investment.

## Updated priority: Russia / China procurement and cheaper first stand

Procurement region: Russia or China/AliExpress. Prefer the following verified seller prices over the US premium-retail Nano stand above. These are displayed Russian offers, not confirmed checkout/delivery quotations. AliExpress lot prices were not verified.

| Part | RUB | Source |
|---|---:|---|
| ESP32-WROOM-32 DevKit, USB-C CH340 | 470 | https://duino.ru/esp32-wifi-bluetooth-type-c-ch340-mikrokontroller/ — 42 units displayed on page |
| SG90 mini positional servo | 180 each | https://arduino54.ru/category/mehanika/servoprivody/ — 359 units displayed |
| 5 V 3 A EU bench adapter, 5.5×2.5 mm DC plug | 350 | https://arduino54.ru/catalog/istochniki-pitaniya/bloki-pitaniya/blok-pitaniya-5v-3a-eu-vilka/ — 16 units displayed |
| Nano V3.0 ATmega328P CH340 compatible board | 310 | https://compacttool.ru/arduino-nano-v30-ch340 — more than 500 displayed |
| Dupont wires, 30 pcs | 110 | Listed on above duino ESP32 product page |
| MAX98357 I2S amplifier | 180 | Listed on above duino ESP32 product page |

**Preferred 2-servo stand:** ESP32 470 + SG90 2×180 + power 350 = **1,180 ₽**; USB data cable, DC screw terminal adapter matching the plug, wires, small fixed mounting bracket and fasteners budget **400–800 ₽** => **1,580–1,980 ₽**, round **1,600–2,000 ₽ before delivery**. One-servo version saves 180 ₽. Start with lightly loaded motion, verify the real 5 V rail; label 3 A on cheap adapters is not a measurement. Servo power is wired directly from the external rail, not through ESP32. No IMU/PCA9685/battery/Pi needed for this stand.

**Nano stand using the proven library path:** replace ESP32 470 with Nano-compatible 310 => **1,420–1,820 ₽**. If the aim is specifically classic Otto, this is an economical option; USB cable is mini-USB instead of USB-C. ESP32 path offers Wi-Fi but requires adapting/testing the movement implementation.

**Chinese manufacturer option:** [XIAO ESP32C3](https://www.seeedstudio.com/Seeed-XIAO-ESP32C3-p-5431.html) is **$4.99** in the official Seeed store. [Official wiki](https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/) documents PWM GPIO and Arduino support. Do not confuse it with the $13.99 S3 Sense; C3 has no camera/microphone. This could replace the controller in the test stand, but a fully tested Otto port for this specific board has not been established.

**Russian planning estimate for complete classic walking Otto (no camera/AI):** Nano-compatible 310 + 4 SG90 720 + HC-SR04/buzzer allowance 200–350 + printed parts/fasteners 600–1,500 + wiring/USB/switch 400–700 + AA holder/rechargeables/charger 1,000–2,000 => **3,230–5,580 ₽**; round **3,500–6,000 ₽**. Most non-core rows are explicit estimates, not current supplier quotations; buy AA/servo voltage combination consistent with selected servo specification. Add first bench supply if not retained from earlier stage.

**Pi-camera extension:** local prices vary strongly. Verified [Amperka listing](https://amperka.ru/collection/promo) shows Pi Zero 2 W **7,290 ₽**, while [ONPAD](https://onpad.ru/catalog/cubie/raspberrypi/raspberrypi/3230.html) shows **8,990 ₽**. Do not imply the international $15 MSRP is the Russian retail price. [Camera Module 2 official page](https://www.raspberrypi.com/products/camera-module-v2/) confirms IMX219 and Zero-specific FPC requirement, but no price; a cheap current Russian V2 offer was not independently established. Therefore prefer the verified international $19.05 Zero + $29.25 Camera3 figures only as foreign price anchors, or use locally sourced camera quotation later. Estimated full Russian Nano+Pi+camera custom build can easily be **15,000–25,000 ₽**, and is poor value compared with an MCU camera option for this tiny gait platform.

## Follow-up review: six-axis Otto-like V1 concept

Parent requested a quick engineering check of 4 leg servos (hip yaw + foot roll), 2 camera pan/tilt servos, Zero 2 W + IMX219, ESP32, MPU6050, 2S LiPo 650–850 mAh and separate 5 V servo/logic converters.

Verdict: plausible research concept, not a proven BOM or guaranteed walking robot. Keep short legs, broad feet, low battery/Pi placement and a very light moving camera head. A **250–300 g total mass goal** is a preliminary engineering constraint, not verified achievable CAD mass or safe payload. Do not add knee joints to the visual depiction: this architecture has no powered knee.

[MG90S manufacturer](https://towerpro.com.tw/product/mg90s-3/) specifies 13.4 g and **1.8 kg·cm stall at 4.8 V**, similar to SG90; metal gears improve durability, not a large torque upgrade. Six proposed servos alone weigh approximately 71.6 g. At 300 g and 3 cm effective lateral lever arm, static roll-joint load is approximately **0.9 kg·cm**, already half nominal stall before dynamic loads. Actual mass, geometry and gait must therefore be checked before claiming walking feasibility. Shorten lever arms and reduce upper-body mass before simply scaling the shell. SG90 head mechanism should have supported axes and a flexible CSI cable loop; cable stiffness also loads the tiny servos.

2S (8.4 V full) into two independent regulated rails is reasonable: **servo 5 V / ≥5 A design target**, **logic 5–5.1 V / 2–3 A**, common ground, separate supply routing. [Raspberry Pi documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#power-supply) lists 2 A recommended PSU capacity for Zero 2 W; 3 A is headroom, not typical draw. Converter continuous/peak ratings, input dropout, heat and servo stall transients require testing. For example [Pololu D24V50F5](https://www.pololu.com/product/2851) supports 2S input but its 5 A rating depends on heat dissipation; its undervoltage lockout is not a LiPo discharge cutoff. Include suitable low-battery cutoff/monitoring, a 2S balance charger and a battery with verified discharge capacity. Capacity alone (650–850 mAh) does not specify allowable current; no runtime can be promised yet.

MPU6050 is useful for tilt/fall detection and telemetry. It does not turn the inherited open-loop gait into a balanced locomotion controller. Program a local command timeout; external AI selects bounded skills, while local control handles completion and stop behaviour. Reuse Otto trajectories as an initial template and retune to mass, servo zeros and mechanics.

Local servo price anchor: four MG90S at 250 ₽ plus two SG90 at 180 ₽ = **1,360 ₽**, versus 720 ₽ for four SG90. Adding the Pi/camera, 2S power system and moving head means the former 3,500–6,000 ₽ bare classic-Otto budget is no longer applicable.
