from models import Location, User, db
from flask_bcrypt import Bcrypt
from app import app
bcrypt = Bcrypt()

db.drop_all()
db.create_all()

User.query.delete()
Location.query.delete()

password = 'password'
hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')


admin = User(id=1,username="admin",email='ktkinsey37@gmail.com',password=hashed_pwd,authority='admin')
no_location_user = User(id=0,username='default_custom',email='fake',password='fake',authority='user')
loc0 = Location(id=0,user_id=0,name='custom_location')
RR = Location(user_id=1,name="Red Rocks",location="Just West of Las Vegas, NV",latitude=36.10579962729647,longitude=-115.46661745232271,description="Tons of different routes on sandstone. Long, desert alpine, hard sport, bouldering, RR has it all. So good that Honnold moved to Vegas to be near it.",is_desert=True,is_snowy=False)
WR = Location(user_id=1,name="Wind River Range",location="In between Lander and Pinedale, WY.",latitude=42.907429448436794,longitude=-109.47754858405727,description="Very alpine location. Includes WY's tallest peak and the famous Cirque of the Towers.",is_desert=False,is_snowy=True)
CV = Location(user_id=1,name="Castle Valley",location="Just East of Moab, UT",latitude=38.6479991772182,longitude=-109.39796378889207,description="Several beautiful desert towers in an amazing location.",is_desert=True,is_snowy=False)
Z = Location(user_id=1,name="Zion",location="An hour east of St George, UT",latitude=37.243142117877014,longitude=-112.95898481212593,description="Zion National Park is home to some amazing climbing, most notably several world-class big wall routes.",is_desert=True,is_snowy=False)
JT = Location(user_id=1,name="Joshua Tree",location="About an hour East of Los Angeles, CA.",latitude=33.98751071670004,longitude=-116.07035986385453,description="Mostly single pitch trad. Notoriously hard climbing. Despite being a desert locale, the rock is quartz monzonite.",is_desert=False,is_snowy=False)
RMNP = Location(user_id=1,name="Rocky Mountain NP",location="A few hours NW of Denver, CO",latitude=40.28002399507943,longitude=-105.66581920087995,description="'The Park' is home to tons of alpine classics, most notably Long's Peak's 'The Diamond'. Watch the weather, it can turn fast and hard.",is_desert=False,is_snowy=True)
Yosemite = Location(user_id=1,name="Yosemite Valley",location="Couple hours East of San Francisco, CA.",latitude=37.744467087009795,longitude= -119.58866707086564,description="The mecca of climbing. Three-thousand foot walls of perfect granite.",is_desert=False,is_snowy=False)

db.session.add(admin)
db.session.add(no_location_user)
db.session.commit()
db.session.add(loc0)
db.session.add(RR)
db.session.add(WR)
db.session.add(CV)
db.session.add(Z)
db.session.add(JT)
db.session.add(RMNP)
db.session.add(Yosemite)

db.session.commit()
