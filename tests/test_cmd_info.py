from factory import app, settings

def test_info():
   assert type(app.info()) is str

