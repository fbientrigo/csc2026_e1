// CSC Latin America 2026 - Track Reconstructor Tests
#include <catch2/catch_test_macros.hpp>
#include <catch2/catch_approx.hpp>

#include "TrackReconstructor.hpp"

using namespace csc2026;
using Catch::Approx;

TEST_CASE("TrackReconstructor default state", "[track]") {
    TrackReconstructor reco;
    REQUIRE(reco.numHits() == 0);
}

TEST_CASE("TrackReconstructor add hits", "[track]") {
    TrackReconstructor reco;
    
    Hit hit1{0.0, 0.0, 0.0, 1.0};
    Hit hit2{1.0, 1.0, 10.0, 1.0};
    
    reco.addHit(hit1);
    REQUIRE(reco.numHits() == 1);
    
    reco.addHit(hit2);
    REQUIRE(reco.numHits() == 2);
}

TEST_CASE("TrackReconstructor clear", "[track]") {
    TrackReconstructor reco;
    
    reco.addHit({0.0, 0.0, 0.0, 1.0});
    reco.addHit({1.0, 1.0, 10.0, 1.0});
    REQUIRE(reco.numHits() == 2);
    
    reco.clear();
    REQUIRE(reco.numHits() == 0);
}

TEST_CASE("TrackReconstructor max hits", "[track]") {
    TrackReconstructor reco(5);  // Max 5 hits
    
    for (int i = 0; i < 10; ++i) {
        reco.addHit({static_cast<double>(i), 0.0, 0.0, 1.0});
    }
    
    REQUIRE(reco.numHits() == 5);  // Should stop at max
}

TEST_CASE("TrackReconstructor empty reconstruction", "[track]") {
    TrackReconstructor reco;
    auto tracks = reco.reconstruct();
    REQUIRE(tracks.empty());
}

TEST_CASE("TrackReconstructor basic reconstruction", "[track]") {
    TrackReconstructor reco;
    
    // Add enough hits for at least one track
    for (int i = 0; i < 10; ++i) {
        reco.addHit({
            static_cast<double>(i) * 0.5,
            static_cast<double>(i) * 0.3,
            static_cast<double>(i) * 10.0,
            1.0
        });
    }
    
    auto tracks = reco.reconstruct();
    REQUIRE(!tracks.empty());
    
    // Each track should have hits
    for (const auto& track : tracks) {
        REQUIRE(track.hits.size() >= 3);
    }
}

TEST_CASE("Track chi2 calculation", "[track]") {
    Track track;
    track.hits = {
        {0.0, 0.0, 0.0, 1.0},
        {1.0, 0.0, 10.0, 1.0},
        {2.0, 0.0, 20.0, 1.0}
    };
    
    // chi2 should be positive
    REQUIRE(track.chi2() > 0.0);
}

TEST_CASE("Track chi2 with single hit", "[track]") {
    Track track;
    track.hits = {{0.0, 0.0, 0.0, 1.0}};
    
    // chi2 with single hit should be 0
    REQUIRE(track.chi2() == 0.0);
}
