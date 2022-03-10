
import json
from flask import session
import requests
import pandas as pd
from ibm_watson import ToneAnalyzerV3, PersonalityInsightsV3, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator



def cut_str_to_bytes(s, max_bytes):
    # cut it twice to avoid encoding potentially GBs of `s` just to get e.g. 10 bytes?
    b = s[:max_bytes]

    if b[-1] & 0b10000000:
        last_11xxxxxx_index = [i for i in range(-1, -5, -1)
                               if b[i] & 0b11000000 == 0b11000000][0]
        # note that last_11xxxxxx_index is negative

        last_11xxxxxx = b[last_11xxxxxx_index]
        if not last_11xxxxxx & 0b00100000:
            last_char_length = 2
        elif not last_11xxxxxx & 0b0010000:
            last_char_length = 3
        elif not last_11xxxxxx & 0b0001000:
            last_char_length = 4

        if last_char_length > -last_11xxxxxx_index:
            # remove the incomplete character
            b = b[:last_11xxxxxx_index]

    return b


def watson_conn():
    '''
    set session variables authenticators and versions for Watson calls
    :return:
    '''
    # open config file and get data
    with open("config.json") as config_data_file:
        config_data = json.load(config_data_file)

    tone_data = config_data['watson']['tone_api']

    tone_auth = IAMAuthenticator(tone_data['apikey'])

    session['tone_analyzer'] = ToneAnalyzerV3(
        version=tone_data['version'],
        authenticator=tone_auth
    )

    session['tone_analyzer'].set_service_url(tone_data['url'])

    return

def watson_conn2():

    apikey = 'OsJZkHGpFZxmFfYOc5dz0dMbXYu6jWdXi76jSgIfG9DP'
    tone_auth = IAMAuthenticator(apikey)

    tone_analyzer = ToneAnalyzerV3(
        version='2017-09-21',
        authenticator=tone_auth
    )

    return tone_analyzer
    #tone_url = 'https://gateway.watsonplatform.net/tone-analyzer/api'
    #tone_analyzer.set_service_url(tone_url)

def analyze(tone_analyzer):
    text = 'Team, I know that times are tough! Product ' \
           'sales have been disappointing for the past three ' \
           'quarters. We have a competitive product, but we ' \
           'need to do a better job of selling it!'

    tone_analysis = tone_analyzer.tone(
        text,
        content_type='text/plain;charset=utf-8',
        sentences=False
    ).get_result()

    print(json.dumps(tone_analysis, indent=2))

    return

if __name__ == '__main__':
    #text = "b'[Uber stole their ideas from Johnny Cab smh \xf0\x9f\xa4\xa6\\u200d\xe2\x99\x82\xef\xb8\x8f , @uceedaddy MJ: Don\xe2\x80\x99t SaaS me bruh, Savings rates are closely tied to Fed Funds Rate, now effectively 0.05%, so it\xe2\x80\x99ll be hard to find much better than\xe2\x80\xa6 , @uceedaddy Forgot to say they want to delete app with perfect match, 48/50, not seen Usual Suspects or Wall-E ! , @uceedaddy He does a lot of Finance satire, @TheAttack5 There\xe2\x80\x99s gotta be a tracking website for how many defective Teslas are created, @stephanPhD Great thread \xf0\x9f\x91\x8d\xf0\x9f\x8f\xbc! We should expect more hybrid models of higher education in future. Large lecture class\xe2\x80\xa6 , @TheAttack5 Venture Capital has too much money to throw away (exhibit A = Sotfbank), @TheAttack5 @Dr_BrianMD Being like 6-3 is most optimal, over that, just hit your head on shit all the time, @TheAttack5 I\xe2\x80\x99ll join and raise avg height, @NeerajKA Can use $300 credit on gas/groceries for rest of 2020, @TheAttack5 I think my iPhone 7 port got worn out, stopped charging completely a month ago. Have an SE now, good to have both options, @uceedaddy The sequel will be me finding a tarantula or snake \xf0\x9f\x98\xb3\xf0\x9f\x98\x96, @TheAttack5 Is that a surgery cone for Dogs?!, @pitdesi @juliey4 Renessaince IPO ETF up 41% in same time period, if @profgalloway hypothetically was Mkt Neutral L\xe2\x80\xa6 , @pitdesi @juliey4 A proper comparison of a unrealistic, not professionally Mgd portfolio of 8 tech stocks, TSLA is\xe2\x80\xa6 , @juliey4 @pitdesi Why October 4th as a Start date? This is such bullshit clickbait haha, @uceedaddy So many grammatical errors, @zoom_us needs to make mute all participants the default option, @lwrncjones I got a 30\xe2\x80\x9d monitor for $200, very much needed, @JohnnyVegas113 RIP to that warehouse on Market st party, @Dr_BrianMD @TheAttack5 Space Jam 2 gonna be wild!, @uceedaddy Idk why they had Lowry and Kemba both in together for so long, @uceedaddy Jones would of won like 9/10 last dunk contests, just this one was sooo crazy good, @Sweekuh My company SVB is right there. Will come for DJ Sweekuh at El Hefe on Mill Ave \xf0\x9f\xa4\x97\xf0\x9f\x8c\xb5, @Sweekuh @Boeing I\xe2\x80\x99m in Scottsdale/Tempe pretty often, get ready for AZ summer!!, My gift to New York City...after moving away 7 months ago\\n, @lwrncjones Soooo hype, ride the Mostert train \xf0\x9f\x9a\x82!!, @JohnnyVegas113 @kgeich @YourNewAsianBFF, @Dr_BrianMD Is Burrow a solid top 5 pick?!, @TheAttack5 Sacramento and San Jose are so freaking dull it\xe2\x80\x99s amazing, Truuueeee, they said Louisville star only though, the disrespect is real!! , When I shop for myself while hungry , @TheAttack5 @kgeich @cjhynes09 @Jferrie23 Up to $5000 per year, that ALMOST covers the interest!, @Dr_BrianMD I would think Dallas with Prescott/Elliott would be a tougher challenge for 49ers Defense. So annoying this rule still exists, @Dr_BrianMD Pac12 represent!, @Dr_BrianMD You think Utah has a chance at making the playoffs?, @Dr_BrianMD That one part of North Dakota really wants to see their Boy, @TheAttack5 He lives in the Ritz Carlton building, only cares about his brand smh, @Dr_BrianMD @Twilliterate88 @kgeich well they ain\xe2\x80\x99t played nobody, TILL now!! Thinking closely beat Packers, toss u\xe2\x80\xa6 , It wont upgrade greatly your career anymore but its good to know the content of the tests , @azinasili @ian_yama , @JohnnyVegas113 would say thats a carry \xf0\x9f\x98\x9c , @azinasili I\xe2\x80\x99m dying at some of these , @Dr_BrianMD Shake shack Chicken sandwich up there as well, @lwrncjones I live in SF now, I been supporting the Dragon (and Louisville \xf0\x9f\x98\x9d) in NBA haha, You don\xe2\x80\x99t subscribe to all at once, you pick 2-3 at a time. Or you share logins...who has time to even watch that m\xe2\x80\xa6 , Fart and Romance modes on Teslas should be a new standard, @Dr_BrianMD Not the Star wars game coming out in a few weeks?!, @azinasili , , My first Earthquake in a long time \xf0\x9f\x99\x84\xf0\x9f\x99\x84\xf0\x9f\x99\x84, All monthly commitments, can always add/subtract the services as desired, very easily. , @AmericanAir I\xe2\x80\x99m not even asking for a refund or to change my flight, I just want to keep return flight of my trip.\xe2\x80\xa6 , @AmericanAir sooo let me get this straight, if I no longer need to fly the first leg of a basic economy round trip\xe2\x80\xa6 , @JohnnyVegas113 Jane* one syllable!!, @azinasili toilets getting revenge , @Dr_BrianMD Be there in a minute, I\xe2\x80\x99m cysting, @Dr_BrianMD Those all work as verbs too\\nMoisting\\nSlopping, If you want to start a scooter company, prerequisites is it has to be a one syllable word\\n\\nLime\\nBird\\nScoot\\nSkip, @JohnnyVegas113 @Dr_BrianMD Home Ownership isn\xe2\x80\x99t always a good idea though....#DrFinance, @AppleSupport your iPhone charging cable stopped working after 3 weeks, pretty defective and disappointing!!, Put this asshole in prison for life , @Dr_BrianMD 10:30pm PST, so Hawaii people MAY watch, Gotta invite Mr Michelob @JohnnyVegas113 , @JohnnyVegas113 @uceedaddy I\xe2\x80\x99m glad I can now wear jeans to work at least \xf0\x9f\x98\x9c, @uceedaddy Better or worse than wearing jeans while running 5s?, I\xe2\x80\x99m looking forward to opening @SoFi Money account. Is the 2.25% APY a promo rate? How does the FDIC insurance work?, @TheAttack5 @Sweekuh @cjhynes09 @Num1HandsomeBoy @Dr_BrianMD @tacoelle__ @bpalms31 \xe2\x80\x9cfuture investment banker\xe2\x80\x9d womp, Still getting used to California\xe2\x80\x99s vendetta against plastic straws, @JohnnyVegas113 SMH I got a dope apartment in the Mission district, no hostel living, Bedroom to myself! \xf0\x9f\xa4\xb7\xf0\x9f\x8f\xbb\\u200d\xe2\x99\x82\xef\xb8\x8f, Berlin Tegel taking the crown from LaGuardia for crappiest airport, @theZorb I also just sweet talked the train guy in Berlin to not give me a ticketing fine \xf0\x9f\x98\x8e, I\xe2\x80\x99m convinced Europeans hate air conditioning and putting ice in drinks, @JohnnyVegas113 Kemba is probably best match, depends what he wants from contract., @princesskelly91 Gotta Add Butter, Sell to drunk college students, massive profit potential , @theZorb @annablankx @kyrstenkam As an Ohio veteran I approve this message, @Dr_BrianMD @TheAttack5 @AbarryE $20M @Twilliterate88 *runs away*, @Dr_BrianMD @TheAttack5 @AbarryE Ben going to get like a 2yr/$2 from Lakers as pittance fee, @TheAttack5 Make Puerto Rico a state and push out Alabama, Whoever conceived of these credit card rebate things should do us a favor and jump off a cliff into a pit of glass, @SwedenDC Sex cult ehhh \xe2\x98\x9d\xef\xb8\x8f, @uceedaddy This guy traveling \xf0\x9f\x91\x80 Air Canada \xf0\x9f\x87\xa8\xf0\x9f\x87\xa6 \xe2\x9c\x88\xef\xb8\x8f Platinum member soon haha, @Dr_BrianMD Should just give people a subscription to DataCamp]'"
    #print(cut_str_to_bytes(text, 128000))

    tone_analyzer = watson_conn2()
    analysis = analyze(tone_analyzer)