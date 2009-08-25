from waveapi import events
from waveapi import model
from waveapi import robot

APP_VERSION = '2'

def OnParticipantsChanged(properties, context):
  """Invoked when any participants have been added/removed."""
  added = properties['participantsAdded']
  for p in added:
    Notify(context)

def OnRobotAdded(properties, context):
  """Invoked when the robot has been added."""
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText("I'm alive! Version" + APP_VERSION)

def OnBlipCreated(properties, context):
  root_wavelet = context.GetRootWavelet()
  for blip in context.GetBlips():
    text = blip.GetDocument().GetText()
    if blip.getCreator()!="contextlinky@appspot.com": # is this neccesary?
      root_wavelet.CreateBlip().GetDocument().SetText("Du sagde: "+text)

def Notify(context):
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText("Hi everybody!")

if __name__ == '__main__':
  myRobot = robot.Robot('contextlinky', 
      image_url='http://contextlinky.appspot.com/icon.png',
      version=APP_VERSION,
      profile_url='http://contextlinky.appspot.com/')
  myRobot.RegisterHandler(events.WAVELET_PARTICIPANTS_CHANGED, OnParticipantsChanged)
  myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
  myRobot.RegisterHandler(events.WAVELET_BLIP_CREATED, OnBlipCreated)
  myRobot.Run()
  