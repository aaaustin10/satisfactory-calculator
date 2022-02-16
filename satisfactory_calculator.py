from collections import OrderedDict
import math

def generate_ngmop3a2_lookup(max_value):
    max_power = math.ceil(math.log(max_value, 2))
    answer = {}
    for power_2 in range(max_power + 1):
        for power_3 in range(max_power + 1):
            result = 2 ** power_2 * 3 ** power_3
            if result <= 2 ** max_power:
                answer[result] = result

    i = 0
    for j in sorted(answer.keys()):
        while i <= j:
            answer[i] = j
            i += 1
    return answer

def ngmop3a2(n):
    n = math.ceil(n)
    """Get the nearest multiple of powers 3 and 2 that is larger than n"""
    if n < 1:
        return 1
    elif n > 2 ** 20:
        raise NotImplementedError('Number is too large for lookup table implementation.')

    lookup_table = getattr(ngmop3a2, 'lookup_table', {})

    try:
        return lookup_table[n]
    except KeyError:
        ngmop3a2.lookup_table = generate_ngmop3a2_lookup(n)

    return ngmop3a2(n)


class ThingRecipe():
    def __init__(self, seconds_to_produce, amount_produced, components, byproducts={}):
        self.components = components
        self.byproducts = byproducts
        self.seconds_to_produce = seconds_to_produce
        self.amount_produced = amount_produced
        self.per_min_mult = self.amount_produced / self.seconds_to_produce * 60

    def building_count(self):
        limiting_factors = []
        min_building_count = None
        for ingredient, count in self.base_units.items():
            building_count = MINING_RATES[ingredient] / (self.per_min_mult * count)
            if min_building_count == building_count:
                limiting_factors.append(ingredient)
            elif min_building_count is None or min_building_count > building_count:
                min_building_count = building_count
                limiting_factors = [ingredient]

        return min_building_count, limiting_factors

    @property
    def base_units(self):
        base_units = getattr(self, '_base_units', {})
        if base_units:
            return base_units

        for component, amount in self.components.items():
            try:
                component_base_units = ALL_THINGS[component].base_units
            except KeyError:
                assert component in MINING_RATES, f"Couldn't find {component!r} in ALL_THINGS or MINING_RATES"
                component_base_units = {component: 1}
            for base_component, base_amount in component_base_units.items():
                base_units.setdefault(base_component, 0)
                base_units[base_component] += (amount / self.amount_produced) * base_amount

        self._base_units = OrderedDict(sorted(base_units.items(), key=lambda x: x[1], reverse=True))
        return self._base_units

    def __str__(self):
        building_count, limiting_ingredients = self.building_count()
        building_count = ngmop3a2(building_count)
        per_base_unit = ', '.join(f'{k}: {v:g}' for k,v in self.base_units.items())
        per_min = ', '.join(f'{v*self.per_min_mult:g} {k}/min' for k,v in self.base_units.items())
        output = f'({per_base_unit})'
        output += f'  [{per_min}]'
        output += f'  {building_count:g} buildings'
        if len(self.base_units) > 1:
            output += ' (limited by %s)' % '/'.join(str(i) for i in limiting_ingredients)
        return output

    def __repr__(self):
        return f'<{self.__class__.__name__}: {str(self)}>'

class ThingPerMin(ThingRecipe):
    def __init__(self, amount_produced_per_min=None, components_per_min={}, byproducts_per_min={}):
        seconds_to_produce = 60 / amount_produced_per_min

        components = {}
        for component, component_per_min in components_per_min.items():
            components[component] = component_per_min / amount_produced_per_min # == components per ThingRecipe

        byproducts = {}
        for byproduct, byproduct_per_min in byproducts_per_min.items():
            byproducts[byproduct] = byproduct_per_min / amount_produced_per_min # == byproducts per ThingRecipe

        super(ThingPerMin, self).__init__(seconds_to_produce, 1, components, byproducts)



# ThingRecipe(seconds_to_produce, amount_produced, {ingredients: count}, {byproducts: count})
# ThingPerMin(amount_produced_per_min, {ingredients: count_per_min}, {byproducts: count_per_min})

ALL_THINGS = {
    'iron-ingot': ThingRecipe(2, 1, {'iron': 1}),
    'iron-plate': ThingRecipe(6, 2, {'iron-ingot': 3}),
    'iron-rod': ThingRecipe(4, 1, {'iron-ingot': 1}),
    'screw': ThingRecipe(6, 4, {'iron-rod': 1}),
    'reinforced-plate': ThingRecipe(12, 1, {'iron-plate': 6, 'screw': 12}),
    'rotor': ThingRecipe(15, 1, {'iron-rod': 5, 'screw': 25}),
    'smart-plating': ThingRecipe(30, 1, {'reinforced-plate': 1, 'rotor': 1}),
    'modular-frame': ThingRecipe(60, 2, {'reinforced-plate': 3, 'iron-rod': 12}),

    'copper-ingot': ThingRecipe(2, 1, {'copper': 1}),
    'wire': ThingRecipe(4, 2, {'copper-ingot': 1}),
    'copper-sheet': ThingRecipe(6, 1, {'copper-ingot': 2}),
    'cable': ThingRecipe(2, 1, {'wire': 2}),
    'beacon': ThingRecipe(8, 1, {'iron-plate': 3, 'iron-rod': 1, 'wire': 15, 'cable': 2}),

    'concrete': ThingRecipe(4, 1, {'limestone': 3}),

    'steel-ingot': ThingRecipe(4, 3, {'steel-iron': 3, 'steel-coal': 3}),
    'steel-beam': ThingRecipe(4, 1, {'steel-ingot': 4}),
    'steel-pipe': ThingRecipe(6, 2, {'steel-ingot': 3}),
    'encased-industrial-beam': ThingRecipe(10, 1, {'steel-beam': 4, 'concrete': 5}),

    'versatile-framework': ThingRecipe(24, 2, {'modular-frame': 1, 'steel-beam': 12}),
    'stator': ThingRecipe(12, 1, {'steel-pipe': 3, 'wire': 8}),
    'automated-wiring': ThingRecipe(24, 1, {'stator': 1, 'cable': 20}),

    'caterium-ingot': ThingRecipe(4, 1, {'caterium': 3}),
    'quickwire': ThingRecipe(5, 5, {'caterium-ingot': 1}),

    'ai-limiter': ThingRecipe(12, 1, {'quickwire': 20, 'copper-sheet': 5}),

    'motor': ThingRecipe(12, 1, {'stator': 2, 'rotor': 2}),

    'fuel': ThingRecipe(6, 4, {'oil': 6}, {'polymer-resin': 3}),
    'plastic': ThingRecipe(6, 2, {'oil': 3}, {'heavy-oil-residue': 1}),
    'rubber': ThingRecipe(6, 2, {'oil': 3}, {'heavy-oil-residue': 2}),
    'residual-fuel': ThingRecipe(6, 4, {'heavy-oil-residue': 6}),
    'residual-plastic': ThingRecipe(6, 2, {'polymer-resin': 6, 'water': 2}),
    'residual-rubber': ThingRecipe(6, 2, {'polymer-resin': 4, 'water': 4}),
    'fuel-generator': ThingPerMin(150, {'fuel': 12}),

    'black-powder': ThingRecipe(8, 1, {'sulfur-coal': 1, 'sulfur': 2}),
    'nobelisk': ThingRecipe(20, 1, {'black-powder': 5, 'steel-pipe': 10}),
    'rifle-cartridge': ThingRecipe(20, 5, {'beacon': 1, 'steel-pipe': 10, 'black-powder': 10, 'rubber': 10}),

    'quartz-crystal': ThingRecipe(8, 3, {'raw-quartz': 5}),
    'silica': ThingRecipe(8, 5, {'raw-quartz': 3}),
    'crystal-oscillator': ThingRecipe(120, 2, {'quartz-crystal': 36, 'cable': 28, 'reinforced-plate': 5}),

    'empty-canister': ThingRecipe(4, 4, {'plastic': 2}),
    'packaged-fuel': ThingRecipe(3, 2, {'fuel': 2, 'empty-canister': 2}),

    'circuit-board': ThingRecipe(8, 1, {'copper-sheet': 2, 'plastic': 4}),
    'computer': ThingRecipe(24, 1, {'circuit-board': 10, 'cable': 9, 'plastic': 18, 'screw': 52}),
    'high-speed-connector': ThingRecipe(16, 1, {'circuit-board': 1, 'cable': 10, 'quickwire': 56}),
    'supercomputer': ThingRecipe(32, 1, {'computer': 2, 'ai-limiter': 2, 'high-speed-connector': 3, 'plastic': 28}),

    'heavy-modular-frame': ThingRecipe(30, 1, {'modular-frame': 5, 'steel-pipe': 15, 'encased-industrial-beam': 5, 'screw': 100}),
    'modular-engine': ThingRecipe(60, 1, {'motor': 2, 'rubber': 15, 'smart-plating': 2}),
    'adaptive-control-unit': ThingPerMin(1, {'automated-wiring': 7.5, 'circuit-board': 5, 'heavy-modular-frame': 1, 'computer': 1}),
    'portable-miner': ThingRecipe(60, 1, {'motor': 1, 'steel-pipe': 4, 'iron-rod': 4, 'iron-plate': 2}),

    'alumina-solution': ThingRecipe(6, 12, {'bauxite': 12, 'water': 18}, {'silica': 5}),
    'aluminum-scrap': ThingRecipe(1, 6, {'alumina-solution': 4, 'bauxite-coal': 2}, {'water': 2}),
    'aluminum-ingot': ThingRecipe(4, 4, {'aluminum-scrap': 6, 'silica': 5}),
    'aluminum-casing': ThingRecipe(2, 2, {'aluminum-ingot': 3}),
    'alclad-aluminum-sheet': ThingRecipe(6, 3, {'aluminum-ingot': 3, 'copper-ingot': 1}),

    'radio-control-unit': ThingRecipe(48, 2, {'aluminum-casing': 32, 'crystal-oscillator': 1, 'computer': 1}),
}


################
# UPDATE THESE #
################
MINING_RATES = {'iron': 240*4, 'copper': 240*2, 'limestone': 240*2, 'steel-iron': 240*2, 'steel-coal': 240*2, 'caterium': 240, 'oil': 600, 'sulfur': 240, 'sulfur-coal': 120*2, 'raw-quartz': 240*2, 'bauxite': 240+120+60, 'bauxite-coal': 240*2, 'water': 120*4, 'polymer-resin': 0, 'heavy-oil-residue': 0}
################


TOWERS = {
    'iron': 'Iron',
    'copper': 'Copper',
    'limestone': 'Limestone',
    'steel-iron': 'Steel',
    'caterium': 'Caterium',
    'oil': 'Oil',
    'polymer-resin': 'Oil',
    'heavy-oil-residue': 'Oil',
    'sulfur': 'Sulfur',
    'raw-quartz': 'Quartz',
    'bauxite': 'Bauxite',
}


grouped_things = {}

for name, var in ALL_THINGS.items():
    group = TOWERS[next(iter(x for x in var.base_units if x in TOWERS))]
    if group not in grouped_things:
        grouped_things[group] = []
    grouped_things[group].append((name, var))

for tower_name, recipes in grouped_things.items():
    print('\n%s tower:' % tower_name)
    print('\n'.join(f'{x[0]}  {x[1]!s}' for x in recipes))
