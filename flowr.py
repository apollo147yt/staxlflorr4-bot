from random import *

# ======= MODIFIER =======
credit = 0
RETURNVALUE = 0.4
SPINS = 200
# =======================

rarityNames = ['Common','Uncommon','Rare','Epic','Legnedary','Mythic','Ultra','Super','Omega','Fabled','Divine','Supreme','Omnipotent','Astral','Celestial','Seraphic','Transcendent','Quantum','Galactic','Eternal','cHa0s','Quantum Shard']
rarityCredits = [-5,1,2,5,10,25,100,250,1000,2500,10000,25000,100000,250000,1000000,2500000,10000000,25000000,100000000,250000000,1000000000,10**20]

mobType = ['Ladybug','Bee','Hornet','Spider','Baby Ant','Worker Ant','Soldier Ant','Queen Ant','Ant Hole','Dandelion','Rock','Centipede','Evil Centipede','Dark Ladybug','Beetle','Scorpion','Cactus','Sandstorm','Fire Ant Burrow','Fire Ant','Fire Queen Ant','Desert Centipede','Locust','Desert Moth','Shiny Ladybug','Crab','Jellyfish','Shell','Starfish','Sponge','Leech','Sea Urchin','Bubble','Plastic','Square','Pentagon']
mobMulti = [1,1.5,1,1,1,1,1,1.5,1,1,1,1,1.5,2,1,1,1,1.5,1,1,2,1.5,1,1,5,1,1,1.5,1,1,1,1,1,3,10,1000]

sacAmount = float(input("Credit Sacrificed amount: "))
luckMultiplier = max(0.207125*(2.34915*sacAmount+463.458)**0.5-4.48083,1)
if sacAmount < 100:
	cycle = 10
	sacAmount = 0
	RETURNVALUE = 1
else:
	print('Sacrificed credits turned into',str(luckMultiplier*10//1/10)+'x Luck Multi')
	if sacAmount < 1000:
		cycle = 3
	elif sacAmount < 10000:
		cycle = 12
	elif sacAmount < 100000:
		cycle = 20
	elif sacAmount < 1000000:
		cycle = 25
	elif sacAmount < 10000000:
		cycle = 30
	else:
		cycle = 35


for i in range(SPINS):
	if i%cycle == 0:
		credit -= round(1.1*sacAmount)
		print()
		print(i,'SPINS\n')
		if sacAmount > 0:
			print('SACRIFICED', round(sacAmount), 'CREDITS\n')
	randomValue = random()
	rng = randomValue/(((luckMultiplier-1)*0.7)+1)
	rarity = 0
	
	if rng < 0.55:
		rarity+=1
	if rng < 0.35:
		rarity+=1
	if rng < 0.2:
		rarity+=1
	if rng < 0.1:
		rarity+=1
	if rng < 0.05:
		rarity+=1
	if rng < 0.02:
		rarity+=1
	if rng < 0.01:
		rarity+=1
	if rng < 0.005:
		rarity+=1
	if rng < 0.0025:
		rarity+=1
	if rng < 0.001:
		rarity+=1
	if rng < 0.00044:
		rarity+=1
	if rng < 0.00014:
		rarity+=1
	if rng < 0.00004:
		rarity+=1
	if rng < 0.00001:
		rarity+=1
	if rng < 0.000004:
		rarity+=1
	if rng < 0.000001:
		rarity+=1
	if rng < 0.0000004:
		rarity+=1
	if rng < 0.0000001:
		rarity+=1
	if rng < 0.00000004:
		rarity+=1
	if rng < 0.00000001:
		rarity+=1
	if rng == 0:
		rarity+=1
		
	mobNum = randint(0,len(mobType)-2)
	if random() < 0.001:
		mobNum = len(mobType)-1
	creditGain = round(rarityCredits[rarity]*mobMulti[mobNum])
	credit += round(RETURNVALUE*creditGain)
	if rarity >= 15:
		print('============ RNG CARRIED ============')
	print(rarityNames[rarity],mobType[mobNum]+',',end=' ')
	if rarityCredits[rarity] > 0:
		print('+',end='')
	print(creditGain,'Credits')
	print('You have',credit,'Credits!')