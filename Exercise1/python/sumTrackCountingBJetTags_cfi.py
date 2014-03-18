import FWCore.ParameterSet.Config as cms

sumTrackCountingBJetTags = cms.EDProducer("JetTagProducer",
    jetTagComputer = cms.string('sumTrackCounting3D'),
    tagInfos = cms.VInputTag(cms.InputTag("impactParameterTagInfos"))
)


