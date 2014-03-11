import FWCore.ParameterSet.Config as cms

shrinkConeTrackCountingHighEffBJetTags = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('shrinkConeTrackCounting3D2nd'),
    tagInfos = cms.VInputTag(cms.InputTag("impactParameterTagInfos"))
)


