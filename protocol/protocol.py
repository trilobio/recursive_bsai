metadata = {"apiLevel": "2.6"}

def run(protocol):
    p20s = protocol.load_instrument("p20_single_gen2", "left", tip_racks=[protocol.load_labware("opentrons_96_filtertiprack_20ul", i) for i in [1, 5, 9]])
    p300s = protocol.load_instrument("p300_single_gen2", "right", tip_racks=[protocol.load_labware("opentrons_96_tiprack_300ul", i) for i in [2, 6]])

    temperature_module = protocol.load_module("temperature module", 10)
    tmp = temperature_module.load_labware("nest_96_wellplate_100ul_pcr_full_skirt")

    tube_rack = protocol.load_labware("opentrons_24_tuberack_generic_2ml_screwcap", 11)
    competent_cells = tube_rack.wells_by_name()["A1"]
    mm = tube_rack.wells_by_name()["A1"]
    pIDMv5K = tube_rack.wells_by_name()["A1"]
    synthetic_vector = tube_rack.wells_by_name()["A1"]
    fragment = tube_rack.wells_by_name()["A1"]
    ctrl_fragment = tube_rack.wells_by_name()["A1"]
    linker_1 = tube_rack.wells_by_name()["A1"]
    linker_2 = tube_rack.wells_by_name()["A1"]
    ctrl_linker_1 = tube_rack.wells_by_name()["A1"]
    ctrl_linker_2 = tube_rack.wells_by_name()["A1"]

    water = protocol.load_labware("nest_12_reservoir_15ml", 8).wells_by_name()["A1"]
    agar_plate = protocol.load_labware("biorad_96_wellplate_200ul_pcr", 4)

    # Resuspension

    # Build
    protocol.pause("Add GoldenGate mastermix")
    p20s.transfer(18, mm, [tmp.wells_by_name(w) for w in ["A1","B1","C1","D1"]])
    
    # Transformation 
