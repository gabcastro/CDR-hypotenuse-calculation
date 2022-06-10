from main import say_hello

def test_say_hello():
  output = say_hello('panda')
  assert output == 'Hello panda!'