metadata = {"apiLevel": "2.6"}

def run(protocol):
    p20s = protocol.load_instrument("p20_single_gen2", "left", tip_racks=[protocol.load_labware("opentrons_96_filtertiprack_20ul", i) for i in [1]])
    p300s = protocol.load_instrument("p300_single_gen2", "right", tip_racks=[protocol.load_labware("opentrons_96_tiprack_300ul", i) for i in [2]])

    temperature_module = protocol.load_module("temperature module", 10)
    tmp = temperature_module.load_labware("nest_96_wellplate_100ul_pcr_full_skirt")

    tube_rack = protocol.load_labware("opentrons_24_tuberack_generic_2ml_screwcap", 11)
    competent_cells = tube_rack.wells_by_name()["A1"]
    mm = tube_rack.wells_by_name()["B1"]
    pIDMv5K_mm = tube_rack.wells_by_name()["C1"]
    # The following 3 are half centrifuge tubes, which are 13.9 shorter than the normal tubes
    synthetic_vector = tube_rack.wells_by_name()["D1"].top(-13.6)
    fragment = tube_rack.wells_by_name()["A2"].top(-13.6)
    ctrl_fragment = tube_rack.wells_by_name()["B2"].top(-13.6)
    linker_1 = tube_rack.wells_by_name()["C2"]
    linker_2 = tube_rack.wells_by_name()["D2"]
    ctrl_linker_1 = tube_rack.wells_by_name()["A3"]
    ctrl_linker_2 = tube_rack.wells_by_name()["B3"]
    pIDMv5K = tube_rack.wells_by_name()["C3"]

    water = protocol.load_labware("nest_1_reservoir_195ml", 8).wells_by_name()["A1"]
    agar_plate = protocol.load_labware("biorad_96_wellplate_200ul_pcr", 4)

    # Resuspension
    # Dilute pIDM
    p300s.transfer(45, water, pIDMv5K)
    p20s.transfer(5, pIDMv5K_mm, pIDMv5K, mix_after=(4, 20))

    # Make 100uM stock solutions of linkers
    p300s.transfer(535, water, linker_1, new_tip="always", mix_after=(15,200))
    p300s.transfer(642, water, linker_2, new_tip="always", mix_after=(15,200))
    p300s.transfer(680, water, ctrl_linker_1, new_tip="always", mix_after=(15,200))
    p300s.transfer(593, water, ctrl_linker_2, new_tip="always", mix_after=(15,200))

    # Make linker solutions
    p300s.transfer(198, [tmp.wells_by_name()[w] for w in ["H12","G12"]], water)
    linker = tmp.wells_by_name()["H12"]
    ctrl_linker = tmp.wells_by_name()["G12"]
    p20s.transfer(1, [linker_1, linker_2], linker, new_tip="always", mix_after=(3,20))
    p20s.transfer(1, [ctrl_linker_1,ctrl_linker_2], ctrl_linker, new_tip="always", mix_after=(3,20))

    # Make 5ng/uL stocks of fragments
    p300s.transfer(50, water, fragment, new_tip="always", mix_after=(5,20))
    p300s.transfer(50, water, ctrl_fragment, new_tip="always", mix_after=(5,20))

    # Build
    # There are 4 plasmids getting built:
    # 1. vector + water (neg control)
    # 2. vector + control insert
    # 3. vector + insert + control linkers
    # 4. vector + insert + experimental linkers
    #
    # Recipe for mm is:
    # 2uL T4 ligase buffer
    # .5ul BsaI
    # .5ul T4 ligase
    # 3uL vector+fragment+linker
    # 14uL H2O
    # 
    # mm is recipe * 5, without vector_fragment+linker:
    # 10uL T4 ligase buffer
    # 2.5uL BsaI
    # 2.5uL T4
    # 70uL H2O
    protocol.pause("Add GoldenGate mastermix")
    p20s.transfer(17, mm, [tmp.wells_by_name()[w] for w in ["A1","B1","C1","D1"]])
    p20s.transfer(1, [dna for dna in [synthetic_vector, water, water]], tmp.wells_by_name()["A1"], new_tip="always")
    p20s.transfer(1, [dna for dna in [synthetic_vector, ctrl_fragment, water]], tmp.wells_by_name()["B1"], new_tip="always")
    p20s.transfer(1, [dna for dna in [synthetic_vector, fragment, ctrl_linker]], tmp.wells_by_name()["C1"], new_tip="always")
    p20s.transfer(1, [dna for dna in [synthetic_vector, fragment, linker]], tmp.wells_by_name()["D1"], new_tip="always")

    # Transform n plate
    samples = 4
    protocol.pause("Incubate, then return to deck")
    temperature_module.set_temperature(8)
    p20s.transfer(15, competent_cells, tmp.wells()[samples:samples+samples+1])
    p20s.transfer(1, tmp.wells()[:samples], tmp.wells()[samples:samples+samples], new_tip='always')
    p20s.transfer(1, pIDMv5K, tmp.wells()[samples+samples])
    protocol.delay(900)
    temperature_module.set_temperature(42)
    protocol.delay(10)
    temperature_module.set_temperature(8)
    protocol.delay(300)

    w = ["{}{}".format(j, k + (i*3)) for i in range(0,4) for j in "ABCDEFGH" for k in range(1,4)]
    i = 0
    for well in tmp.wells()[samples:samples+samples+1]:
        for j in range(0,3):
            t = agar_plate.wells_by_name()[w[i]]
            i+=1
            p20s.pick_up_tip()
            if j != 0:
                p20s.transfer(7.5, water, well, new_tip='never')
            p20s.mix(2,4,well)
            p20s.aspirate(7.5, well)
            p20s.move_to(t.top(6))
            p20s.dispense(6.5)
            p20s.move_to(t.bottom())
            p20s.move_to(t.top())
            p20s.drop_tip()
    temperature_module.deactivate()
