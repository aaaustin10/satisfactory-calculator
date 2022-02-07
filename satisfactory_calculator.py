class Thing():
    def __init__(self, name, components={}):
        self.name = name
        if self.name in components:
            raise Exception('Component cannot be made of itself.')
        assert all(isinstance(c, self.__class__) for c in components)
        self.components = components

    def resolve(self):
        if len(self.components) == 0:
            return {self: 1}

        base_units = {}
        for component, amount in self.components.items():
            component_base_units = component.resolve()
            for base_component, base_amount in component_base_units.items():
                base_units.setdefault(base_component, 0)
                base_units[base_component] += amount * base_amount

        for k, v in base_units.items():
           base_units[k] = round(v, 10)
        return base_units

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<{self.__class__.__name__}: {str(self)}>'

iron_ore = Thing('iron-ore')
iron_ingot = Thing('iron-ingot', {iron_ore: 1})
iron_plate = Thing('iron-plate', {iron_ingot: 1.5})
iron_rod = Thing('iron-rod', {iron_ingot: 1})
screw = Thing('screw', {iron_rod: .25})
reinforced_plate = Thing('reinforced-plate', {iron_plate: 6, screw: 12})
rotor = Thing('rotor', {iron_rod: 5, screw: 25})
smart_plating = Thing('smart-plating', {reinforced_plate: 1, rotor: 1})
modular_frame = Thing('modular-frame', {reinforced_plate: 1.5, iron_rod: 6})

copper_ore = Thing('copper-ore')
copper_ingot = Thing('copper-ingot', {copper_ore: 1})
wire = Thing('wire', {copper_ingot: .5})
copper_sheet = Thing('copper-sheet', {copper_ingot: 2})
cable = Thing('cable', {wire: 2})

limestone = Thing('limestone')
concrete = Thing('concrete', {limestone: 3})

coal = Thing('coal')
steel_ingot = Thing('steel-ingot', {iron_ore: 1, coal: 1})
steel_beam = Thing('steel-beam', {steel_ingot: 4})
steel_pipe = Thing('steel-pipe', {steel_ingot: 3/2})
encased_steel_beam = Thing('encased-steel-beam', {steel_beam: 4, concrete: 5})

versatile_framework = Thing('versatile-framework', {modular_frame: 1, steel_beam: 12})
stator = Thing('stator', {steel_pipe: 3, wire: 8})
automated_wiring = Thing('automated-wiring', {stator: 1, cable: 20})

caterium_ore = Thing('caterium-ore')
caterium_ingot = Thing('caterium-ingot', {caterium_ore: 3})
quickwire = Thing('quickwire', {caterium_ingot: 1/5})

ai_limiter = Thing('ai-limiter', {quickwire: 20, copper_sheet: 5})

motor = Thing('motor', {stator: 2, rotor: 2})

plastic = Thing('plastic')
circuit_board = Thing('circuit-board', {plastic: 4, copper_sheet: 2})
computer = Thing('computer', {circuit_board: 10, cable: 9, plastic: 18, screw: 52})
high_speed_connector = Thing('high-speed-connector', {circuit_board: 1, cable: 10, quickwire: 56})

heavy_modular_frame = Thing('heavy-modular-frame', {modular_frame: 5, steel_pipe: 15, encased_steel_beam: 5, screw: 100})
adaptive_control_unit = Thing('adaptive-control-unit', {automated_wiring: 7.5, circuit_board: 5, heavy_modular_frame: 1, computer: 1})

# print thing
pt = lambda t: print(t, t.resolve())

pt(iron_ore)
pt(iron_ingot)
pt(iron_plate)
pt(iron_rod)
pt(screw)
pt(reinforced_plate)
pt(rotor)
pt(smart_plating)
pt(modular_frame)

pt(copper_ingot)
pt(wire)
pt(cable)
pt(copper_sheet)

pt(steel_beam)
pt(steel_pipe)
pt(encased_steel_beam)

pt(versatile_framework)
pt(stator)
pt(automated_wiring)

pt(caterium_ore)
pt(caterium_ingot)
pt(quickwire)
pt(ai_limiter)

pt(motor)
pt(heavy_modular_frame)
pt(adaptive_control_unit)

pt(high_speed_connector)
