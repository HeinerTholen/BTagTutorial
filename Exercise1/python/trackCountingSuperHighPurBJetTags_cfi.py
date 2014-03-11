import FWCore.ParameterSet.Config as cms

trackCountingSuperHighPurBJetTags = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('trackCounting3D4th'),
    tagInfos = cms.VInputTag(cms.InputTag("impactParameterTagInfos"))
)


