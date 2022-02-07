from collections import OrderedDict


class Thing():
    def __init__(self, name, components={}):
        self.name = name
        if self.name in components:
            raise Exception('Component cannot be made of itself.')
        assert all(isinstance(c, self.__class__) for c in components)
        self.components = components
        self.base_units = self._resolve()

    def _resolve(self):
        if len(self.components) == 0:
            return {self: 1}

        base_units = {}
        for component, amount in self.components.items():
            component_base_units = component.base_units
            for base_component, base_amount in component_base_units.items():
                base_units.setdefault(base_component, 0)
                base_units[base_component] += amount * base_amount

        base_units = OrderedDict(sorted(base_units.items(), key=lambda x: x[1], reverse=True))
        return base_units

    def __str__(self):
        if len(self.components) == 0:
            return self.name
        per_base_unit = ', '.join(f'{k}: {v:g}' for k,v in self.base_units.items())
        output = f'{self.name}'
        output += f'  ({per_base_unit})'
        return output

    def __repr__(self):
        return f'<{self.__class__.__name__}: {str(self)}>'

iron_ore = Thing('iron')
iron_ingot = Thing('iron-ingot', {iron_ore: 1})
iron_plate = Thing('iron-plate', {iron_ingot: 1.5})
iron_rod = Thing('iron-rod', {iron_ingot: 1})
screw = Thing('screw', {iron_rod: .25})
reinforced_plate = Thing('reinforced-plate', {iron_plate: 6, screw: 12})
rotor = Thing('rotor', {iron_rod: 5, screw: 25})
smart_plating = Thing('smart-plating', {reinforced_plate: 1, rotor: 1})
modular_frame = Thing('modular-frame', {reinforced_plate: 1.5, iron_rod: 6})

copper_ore = Thing('copper')
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

caterium_ore = Thing('caterium')
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



grouped_things = {}

for var in dict(locals()).values():
    if isinstance(var, Thing):
        if len(var.components) > 0:
            group = next(iter(var.base_units))
            if group not in grouped_things:
                grouped_things[group] = []
            grouped_things[group].append(var)

for k,v in grouped_things.items():
    print('\n%s tower:' % k)
    print('\n'.join(str(x) for x in v))
