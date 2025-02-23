import tornado.ioloop
import tornado.web
import tornado.websocket
import mtvserverutils
from dotenv import load_dotenv

MTVMEDIA = mtvserverutils.Media()
load_dotenv()

class CORSMiddleware(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def options(self):
        self.set_status(204)
        self.finish()

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        self.clients.add(self)
        print("WebSocket opened")

    def on_message(self, message):
        if message == "add":
            # Add a song to the playlist
            print("Song added")
        elif message == "play":
            # Start playback
            print("Playback started")
        elif message == "pause":
            # Pause playback
            print("Playback paused")
        elif message == "stop":
            # Stop playback
            print("Playback stopped")

    def on_close(self):
        self.clients.remove(self)
        print("WebSocket closed")

    def check_origin(self, origin):
        return True  # Allow all origins

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Index Page")

class ActionHandler(tornado.web.RequestHandler):
    def get(self):
        action_data = MTVMEDIA.action()
        self.write(dict(actiondata=action_data))

class ArnoldHandler(tornado.web.RequestHandler):
    def get(self):
        arnold_data = MTVMEDIA.arnold()
        self.write(dict(arnolddata=arnold_data))

class BruceLeeHandler(tornado.web.RequestHandler):
    def get(self):
        brucelee_data = MTVMEDIA.brucelee()
        self.write(dict(bruceleedata=brucelee_data))

class BruceWillisHandler(tornado.web.RequestHandler):
    def get(self):
        brucewillis_data = MTVMEDIA.brucewillis()
        self.write(dict(brucewillisdata=brucewillis_data))

class BuzzHandler(tornado.web.RequestHandler):
    def get(self):
        buzz_data = MTVMEDIA.buzz()
        self.write(dict(buzzdata=buzz_data))

class CartoonsHandler(tornado.web.RequestHandler):
    def get(self):
        cartoons_data = MTVMEDIA.cartoons()
        self.write(dict(cartoonsdata=cartoons_data))

class CharlieBrownHandler(tornado.web.RequestHandler):
    def get(self):
        charliebrown_data = MTVMEDIA.charliebrown()
        self.write(dict(charliebrowndata=charliebrown_data))

class ChuckNorrisHandler(tornado.web.RequestHandler):
    def get(self):
        chucknorris_data = MTVMEDIA.chucknorris()
        self.write(dict(chucknorrisdata=chucknorris_data))

class ComedyHandler(tornado.web.RequestHandler):
    def get(self):
        comedy_data = MTVMEDIA.comedy()
        self.write(dict(comedydata=comedy_data))

class DramaHandler(tornado.web.RequestHandler):
    def get(self):
        drama_data = MTVMEDIA.drama()
        self.write(dict(dramadata=drama_data))

class DocumentaryHandler(tornado.web.RequestHandler):
    def get(self):
        documentary_data = MTVMEDIA.documentary()
        self.write(dict(documentarydata=documentary_data))

class FantasyHandler(tornado.web.RequestHandler):
    def get(self):
        fantasy_data = MTVMEDIA.fantasy()
        self.write(dict(fantasydata=fantasy_data))

class GhostBustersHandler(tornado.web.RequestHandler):
    def get(self):
        ghostbusters_data = MTVMEDIA.ghostbusters()
        self.write(dict(ghostbustersdata=ghostbusters_data))

class GodzillaHandler(tornado.web.RequestHandler):
    def get(self):
        godzilla_data = MTVMEDIA.godzilla()
        self.write(dict(godzilladata=godzilla_data))

class HarrisonFordHandler(tornado.web.RequestHandler):
    def get(self):
        harrisonford_data = MTVMEDIA.harrisonford()
        self.write(dict(harrisonforddata=harrisonford_data))

class HarryPotterHandler(tornado.web.RequestHandler):
    def get(self):
        harrypotter_data = MTVMEDIA.harrypotter()
        self.write(dict(harrypotterdata=harrypotter_data))

class HellBoyHandler(tornado.web.RequestHandler):
    def get(self):
        hellboy_data = MTVMEDIA.hellboy()
        self.write(dict(hellboydata=hellboy_data))

class IndianaJonesHandler(tornado.web.RequestHandler):
    def get(self):
        indianajones_data = MTVMEDIA.indianajones()
        self.write(dict(indianajonesdata=indianajones_data))

class JamesBondHandler(tornado.web.RequestHandler):
    def get(self):
        jamesbond_data = MTVMEDIA.jamesbond()
        self.write(dict(jamesbonddata=jamesbond_data))

class JohnWayneHandler(tornado.web.RequestHandler):
    def get(self):
        johnwayne_data = MTVMEDIA.johnwayne()
        self.write(dict(johnwaynedata=johnwayne_data))

class JohnWickHandler(tornado.web.RequestHandler):
    def get(self):
        johnwick_data = MTVMEDIA.johnwick()
        self.write(dict(johnwickdata=johnwick_data))

class JurassicParkHandler(tornado.web.RequestHandler):
    def get(self):
        jurassicpark_data = MTVMEDIA.jurassicpark()
        self.write(dict(jurassicparkdata=jurassicpark_data))

class KevinCostnerHandler(tornado.web.RequestHandler):
    def get(self):
        kevincostner_data = MTVMEDIA.kevincostner()
        self.write(dict(kevincostnerdata=kevincostner_data))

class KingsmanHandler(tornado.web.RequestHandler):
    def get(self):
        kingsman_data = MTVMEDIA.kingsman()
        self.write(dict(kingsmandata=kingsman_data))

class LegoHandler(tornado.web.RequestHandler):
    def get(self):
        lego_data = MTVMEDIA.lego()
        self.write(dict(legodata=lego_data))

class MenInBlackHandler(tornado.web.RequestHandler):
    def get(self):
        meninblack_data = MTVMEDIA.meninblack()
        self.write(dict(meninblackdata=meninblack_data))

class MinionsHandler(tornado.web.RequestHandler):
    def get(self):
        minions_data = MTVMEDIA.minions()
        self.write(dict(minionsdata=minions_data))

class MiscHandler(tornado.web.RequestHandler):
    def get(self):
        misc_data = MTVMEDIA.misc()
        self.write(dict(miscdata=misc_data))

class NicolasCageHandler(tornado.web.RequestHandler):
    def get(self):
        nicolascage_data = MTVMEDIA.nicolascage()
        self.write(dict(nicolascagedata=nicolascage_data))

class OldiesHandler(tornado.web.RequestHandler):
    def get(self):
        oldies_data = MTVMEDIA.oldies()
        self.write(dict(oldiesdata=oldies_data))

class PandasHandler(tornado.web.RequestHandler):
    def get(self):
        pandas_data = MTVMEDIA.pandas()
        self.write(dict(pandasdata=pandas_data))

class PiratesHandler(tornado.web.RequestHandler):
    def get(self):
        pirates_data = MTVMEDIA.pirates()
        self.write(dict(piratesdata=pirates_data))

class RiddickHandler(tornado.web.RequestHandler):
    def get(self):
        riddick_data = MTVMEDIA.riddick()
        self.write(dict(riddickdata=riddick_data))

class SciFiHandler(tornado.web.RequestHandler):
    def get(self):
        scifi_data = MTVMEDIA.scifi()
        self.write(dict(scifidata=scifi_data))

class StaloneHandler(tornado.web.RequestHandler):
    def get(self):
        stalone_data = MTVMEDIA.stalone()
        self.write(dict(stalonedata=stalone_data))

class StarTrekHandler(tornado.web.RequestHandler):
    def get(self):
        startrek_data = MTVMEDIA.startrek()
        self.write(dict(startrekdata=startrek_data))

class StarWarsHandler(tornado.web.RequestHandler):
    def get(self):
        starwars_data = MTVMEDIA.starwars()
        self.write(dict(starwarsdata=starwars_data))

class SuperHeroesHandler(tornado.web.RequestHandler):
    def get(self):
        superheroes_data = MTVMEDIA.superheroes()
        self.write(dict(superheroesdata=superheroes_data))

class TinkerBellHandler(tornado.web.RequestHandler):
    def get(self):
        tinkerbell_data = MTVMEDIA.tinkerbell()
        self.write(dict(tinkerbelldata=tinkerbell_data))

class TomCruiseHandler(tornado.web.RequestHandler):
    def get(self):
        tomcruise_data = MTVMEDIA.tomcruise()
        self.write(dict(tomcruisedata=tomcruise_data))

class TransformersHandler(tornado.web.RequestHandler):
    def get(self):
        transformers_data = MTVMEDIA.transformers()
        self.write(dict(transformersdata=transformers_data))

class TremorsHandler(tornado.web.RequestHandler):
    def get(self):
        tremors_data = MTVMEDIA.tremors()
        self.write(dict(tremorsdata=tremors_data))

class TheRockHandler(tornado.web.RequestHandler):
    def get(self):
        therock_data = MTVMEDIA.therock()
        self.write(dict(therockdata=therock_data))

class VanDamHandler(tornado.web.RequestHandler):
    def get(self):
        vandam_data = MTVMEDIA.vandam()
        self.write(dict(vandamdata=vandam_data))

class XMenHandler(tornado.web.RequestHandler):
    def get(self):
        xmen_data = MTVMEDIA.xmen()
        self.write(dict(xmendata=xmen_data))

class alteredcarbons1Handler(tornado.web.RequestHandler):
    def get(self):
        alteredcarbons1_data = MTVMEDIA.alteredcarbons1()
        self.write(dict(alteredcarbons1data=alteredcarbons1_data))

class alteredcarbons2Handler(tornado.web.RequestHandler):
    def get(self):
        alteredcarbons2_data = MTVMEDIA.alteredcarbons2()
        self.write(dict(alteredcarbons2data=alteredcarbons2_data))





class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/action", ActionHandler),
            (r"/arnold", ArnoldHandler),
            (r"/brucelee", BruceLeeHandler),
            (r"/brucewillis", BruceWillisHandler),
            (r"/buzz", BuzzHandler),
            (r"/cartoons", CartoonsHandler),
            (r"/charliebrown", CharlieBrownHandler),
            (r"/chucknorris", ChuckNorrisHandler),
            (r"/comedy", ComedyHandler),
            (r"/drama", DramaHandler),
            (r"/documentary", DocumentaryHandler),
            (r"/fantasy", FantasyHandler),
            (r"/ghostbusters", GhostBustersHandler),
            (r"/godzilla", GodzillaHandler),
            (r"/harrisonford", HarrisonFordHandler),
            (r"/harrypotter", HarryPotterHandler),
            (r"/hellboy", HellBoyHandler),
            (r"/indianajones", IndianaJonesHandler),
            (r"/jamesbond", JamesBondHandler),
            (r"/johnwayne", JohnWayneHandler),
            (r"/johnwick", JohnWickHandler),
            (r"/jurassicpark", JurassicParkHandler),
            (r"/kevincostner", KevinCostnerHandler),
            (r"/kingsman", KingsmanHandler),
            (r"/lego", LegoHandler),
            (r"/meninblack", MenInBlackHandler),
            (r"/minions", MinionsHandler),
            (r"/misc", MiscHandler),
            (r"/nicolascage", NicolasCageHandler),
            (r"/oldies", OldiesHandler),
            (r"/pandas", PandasHandler),
            (r"/pirates", PiratesHandler),
            (r"/riddick", RiddickHandler),
            (r"/scifi", SciFiHandler),
            (r"/stalone", StaloneHandler),
            (r"/startrek", StarTrekHandler),
            (r"/starwars", StarWarsHandler),
            (r"/superheroes", SuperHeroesHandler),
            (r"/tinkerbell", TinkerBellHandler),
            (r"/tomcruise", TomCruiseHandler),
            (r"/transformers", TransformersHandler),
            (r"/tremors", TremorsHandler),
            (r"/therock", TheRockHandler),
            (r"/vandam", VanDamHandler),
            (r"/xmen", XMenHandler),
            (r"/websocket", WebSocketHandler),
        ]
        settings = {
            "default_handler_class": CORSMiddleware,
        }
        super(Application, self).__init__(handlers, **settings)

if __name__ == "__main__":
    load_dotenv()
    app = Application()
    app.listen(7777)
    tornado.ioloop.IOLoop.current().start()