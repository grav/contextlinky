from waveapi import events
from waveapi import model
from waveapi import robot
from waveapi.ops import OpBuilder
from google.appengine.api import urlfetch

APP_VERSION = '7'

def OnParticipantsChanged(properties, context):
  """Invoked when any participants have been added/removed."""
  added = properties['participantsAdded']
  for p in added:
    Notify(context)

def OnRobotAdded(properties, context):
  """Invoked when the robot has been added."""
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText("I'm alive! Version" + APP_VERSION)

def OnBlipSubmitted(properties, context):
  for blip in context.GetBlips():
    if blip.GetCreator()!="contextlinky@appspot.com": # is this neccesary?
      text = blip.GetDocument().GetText()
      reply = "Auf <b>Deutsch</b>: " + AddContext(text)
      response_blip = blip.CreateChild()
      #  def DocumentAppendMarkup(self, wave_id, wavelet_id, blip_id, content):
      OpBuilder(context).DocumentAppendMarkup(blip.waveId, blip.waveletId, response_blip.GetId(), reply)

def AddContext(text):
  url = "http://dev.wikipedia-lab.org/WikipediaOntologyAPIv3/Service.asmx"
  method = "POST"
  headers = {
    "Soapaction": "http://tempuri.org/GetTopCandidateIDFromKeyword"
  }

  payload = """
<?xml version="1.0" encoding="UTF-8"?>

  <SOAP-ENV:Envelope

    xmlns:xsd="http://www.w3.org/2001/XMLSchema"

    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

    xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/"

    SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"

    xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">

      <SOAP-ENV:Body>

        <GetCandidatesFromKeyword xmlns="http://tempuri.org/">

          <Keyword xsi:type="xsd:string">%s</Keyword>

          <language xsi:type="xsd:string">English</language>

        </GetCandidatesFromKeyword>

      </SOAP-ENV:Body>

    </SOAP-ENV:Envelope>
""" % text.strip()

  result = urlfetch.fetch(url, payload, method, headers)

  return str(result.status_code)

  if result.status_code == 200:
    return result.content
  else:
    return payload


def Notify(context):
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText("Hi everybody!")

if __name__ == '__main__':
  myRobot = robot.Robot('contextlinky', 
      image_url='http://contextlinky.appspot.com/assets/icon.png',
      version=APP_VERSION,
      profile_url='http://contextlinky.appspot.com/')
  myRobot.RegisterHandler(events.WAVELET_PARTICIPANTS_CHANGED, OnParticipantsChanged)
  myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
  myRobot.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
  myRobot.Run()
  