import FWCore.ParameterSet.Config as cms

trackCountingSuperHighEffBJetTags = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('trackCounting3D1st'),
    tagInfos = cms.VInputTag(cms.InputTag("impactParameterTagInfos"))
)


