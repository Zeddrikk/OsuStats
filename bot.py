import discord
from discord.ext import commands
from aiohttp import request


#create client
client = commands.Bot(command_prefix='!')






#arefresh token on startup attempt

@client.event

async def on_ready():
	general_channel = client.get_channel(771587437452328964)

	with open('RefreshToken.txt','r') as reader:
		refresh = reader.read()
		lines=reader.readlines()
		reader.close()

	del lines

		

	


	URL = "https://osu.ppy.sh/oauth/token"
	paramater = {
		'grant_type': 'refresh_token',
		'client_id':'3636',
		'refresh_token':str(refresh),
		'client_secret':'pYZ8IhrzUBWs3ha7d2Ox561Q3ahcHhfF2EuU0GFV'

		


		}
	#tokens = request.post(URL,data=paramater)

	


	async with request("POST", URL, data=paramater) as response:
		if response.status == 200:
			token = await response.json()
			newToken = token["refresh_token"]
			authToken = token["access_token"]
			await general_channel.send("Hello, Token Refreshed!")
		else:
			await general_channel.send("idk why")
			await general_channel.send(response.status)
			await general_channel.send(response.json)
	
	



	with open('RefreshToken.txt','w') as writer:
		writer.write(newToken)
		writer.close()
	with open('AccessToken.txt','w') as write:
		write.write(authToken)
		write.close()












#////////////////////////////////////////////////////
#osu command, hopefully
#////////////////////////////////////////////////////





@client.command(name='osu')
async def osu(context,uName : str):
	#setup API
	with open('AccessToken.txt','r') as reader:
		accessToken = reader.read()
		reader.close()
	URL = "https://osu.ppy.sh/api/v2/users/" + uName
	header = {'Authorization' : "Bearer " + str(accessToken)}
	async with request("GET",URL, headers=header) as response:
		if response.status == 200:
			data = await response.json()
		elif response.status == 401:
			await context.send("Token Expired")
		else:
			await context.send("Invalid Username")




	#Top Play
	profile_id = data["id"]
	bestURL = "https://osu.ppy.sh/api/v2/users/" + str(profile_id) + "/scores/best"
	
	async with request("GET",bestURL,headers = header) as response:
		if response.status == 200:
			temp = await response.json()
		else:
			await context.message.channel.send(bestURL)
			await context.send(response.status)

			await context.send("error")


	



	




	#COUNTRIES BABy (im dead inside pls help)
	countryPic =  {
		'US':":flag_us:",
		'RU':":flag_ru:",
		'DE':":flag_de:",
		'PL':":flag_pl:",
		'FR':":flag_fr:",
		'JP':":flag_jp:",
		'CA':":flag_ca:",
		'BR':":flag_br:",
		'GB':":flag_gb:",
		'TW':":flag_tw:",
		'KR':":flag_kr:",
		'AU':":flag_au:",
		'CH':":flag_cn:",
		'PH':":flag_ph:",
		'ID':":flag_id:",
		'UA':":flag_ua:",
		'CL':":flag_cl:",
		'AR':":flag_ar:",
		'FI':":flag_fi:",
		'MY':":flag_my:",
		'SG':":flag_sg:",
		'MX':":flag_mx:",
		'NL':":flag_nl:",
		'ES':":flag_es:",
		'HK':":flag_HK:",
		'IT':":flag_it:",
		'SE':":flag_se:",
		'TH':":flag_th:",
		'VN':":flag_vn:",
		'CZ':":flag_cz:",
		'NO':":flag_no:",
		'TR':":flag_tr:",
		'AT':":flag_at:",
		'BE':":flag_be:",
		'BY':":flag_by:",
		'PT':":flag_pt:",
		'RO':":flag_ro:",
		'HU':":flag_hu:",
		'KZ':":flag_kz:",
		'DK':":flag_dk:",
		'PE':":flag_pe:",
		'LI':":flag_li:",
		'CO':":flag_co:",
		'IL':":flag_il:",
		'CH':":flag_ch:",
		'EE':":flag_ee:",
		'BG':":flag_bg:",
		'GR':":flag_gr:",
		'SK':":flag_sk:",
		'MA':":flag_ma:"
		}











	#setup Variables
	stats = data["statistics"]
	rank = stats["rank"]
	gRank = rank["global"]
	cRank = rank["country"]
	avatarURL = str(data["avatar_url"])
	
	profileURL = "https://osu.ppy.sh/users/" + str(profile_id)
	uName = data["username"]
	country = data["country_code"]
	country = countryPic.get(country)
	acc = float(stats["hit_accuracy"])
	pp = int(stats["pp"])

	if(avatarURL == "/images/layout/avatar-guest.png"):
		avatarURL = "https://a.ppy.sh/"







#setup embed

	
	
	osu = discord.Embed(title = "Osu! | " + uName, color=0xFF66AA, url= profileURL)
	osu.set_thumbnail(url =avatarURL)
	osu.add_field(name="Rank", value=str(country) + "-"+str(cRank) + "  :globe_with_meridians:- " + str(gRank), inline= False)
	osu.add_field(name="Accuracy	PP", value = str(acc)  +"\u200B \u200B \u200B \u200B \u200B \u200B" + str(pp), inline = False)




	await context.message.channel.send(embed=osu)










#top play variables

	top = temp[0]
	acc = 100 * top["accuracy"]
	pp = top["pp"]

	beatmapStats = top["beatmap"]
	beatmapName = top["beatmapset"]
	artist = beatmapName["artist"]
	name = beatmapName["title"]
	mapurl = beatmapStats["url"]
	diff = beatmapStats["version"]
	covers = beatmapName["covers"]
	picURL = covers["card"]
	stars = beatmapStats["difficulty_rating"]



	modemotes = {
		'HD':"772081586232492033",
		'HR':"772081598970855485",
		'DT':"772081528695291904",
		'FL':"772081559289200660",
		'HT':"772081610866425897",
		'EZ':"772081543794655243",
		'SD':"772081292141395989",
		'NC':"772092311252631552"
	}

#set mods
	mods_stars = ":star: " +str(stars) + "\u200B \u200B \u200B \u200B \u200B \u200B" 
	modstest = top["mods"]
	for mods in  top["mods"]:
		mods = "<:" + mods + ":" + modemotes.get(mods)+">"
		mods_stars += str(mods)
		
	if modstest ==[]:
		mods_stars += "None"
	

	
		
	
	




	





	play = discord.Embed(title = "**Top Play: " +  name +" by " + artist +": " + diff+ "**", url =mapurl,color=0xFF66AA )
	play.add_field(name = "Stars \u200B \u200B \u200B \u200B \u200B \u200B \u200B \u200B \u200B \u200B Mods", value =  mods_stars)
	play.add_field(name = "PP" , value = str(pp))

	play.set_image(url =picURL )





	await context.send(embed = play)
	
	




#run on server

client.run("NNDc2ODI4OTgyMjg1OTU5MTg5.W2s_mA.6FWONjTrBdBVbDh-KtMkHeon068")
