define([
    'legacyRegistry',

    '../src/adapter/bundle',
    '../src/api/objects/bundle',

    '../example/builtins/bundle',
    '../example/composite/bundle',
    '../example/eventGenerator/bundle',
    '../example/export/bundle',
    '../example/extensions/bundle',
    '../example/forms/bundle',
    '../example/generator/bundle',
    '../example/identity/bundle',
    '../example/imagery/bundle',
    '../example/mobile/bundle',
    '../example/msl/bundle',
    '../example/notifications/bundle',
    '../example/persistence/bundle',
    '../example/plotOptions/bundle',
    '../example/policy/bundle',
    '../example/profiling/bundle',
    '../example/scratchpad/bundle',
    '../example/taxonomy/bundle',
    '../example/worker/bundle',

    '../platform/commonUI/about/bundle',
    '../platform/commonUI/browse/bundle',
    '../platform/commonUI/dialog/bundle',
    '../platform/commonUI/edit/bundle',
    '../platform/commonUI/formats/bundle',
    '../platform/commonUI/general/bundle',
    '../platform/commonUI/inspect/bundle',
    '../platform/commonUI/mobile/bundle',
    '../platform/commonUI/notification/bundle',
    '../platform/commonUI/regions/bundle',
    '../platform/commonUI/themes/espresso/bundle',
    '../platform/commonUI/themes/snow/bundle',
    '../platform/containment/bundle',
    '../platform/core/bundle',
    '../platform/entanglement/bundle',
    '../platform/execution/bundle',
    '../platform/exporters/bundle',
    '../platform/features/clock/bundle',
    '../platform/features/conductor/bundle',
    '../platform/features/imagery/bundle',
    '../platform/features/layout/bundle',
    '../platform/features/pages/bundle',
    '../platform/features/plot/bundle',
    '../platform/features/static-markup/bundle',
    '../platform/features/table/bundle',
    '../platform/features/timeline/bundle',
    '../platform/forms/bundle',
    '../platform/framework/bundle',
    '../platform/framework/src/load/Bundle',
    '../platform/identity/bundle',
    '../platform/persistence/aggregator/bundle',
    '../platform/persistence/couch/bundle',
    '../platform/persistence/elastic/bundle',
    '../platform/persistence/local/bundle',
    '../platform/persistence/queue/bundle',
    '../platform/policy/bundle',
    '../platform/representation/bundle',
    '../platform/search/bundle',
    '../platform/status/bundle',
    '../platform/telemetry/bundle',
], function (legacyRegistry) {

    var DEFAULTS = [
        'src/adapter',
        'src/api/objects',
        'platform/framework',
        'platform/core',
        'platform/representation',
        'platform/commonUI/about',
        'platform/commonUI/browse',
        'platform/commonUI/edit',
        'platform/commonUI/dialog',
        'platform/commonUI/formats',
        'platform/commonUI/general',
        'platform/commonUI/inspect',
        'platform/commonUI/mobile',
        'platform/commonUI/themes/espresso',
        'platform/commonUI/notification',
        'platform/containment',
        'platform/execution',
        'platform/exporters',
        'platform/telemetry',
        'platform/features/clock',
        'platform/features/imagery',
        'platform/features/layout',
        'platform/features/pages',
        'platform/features/plot',
        'platform/features/timeline',
        'platform/features/table',
        'platform/forms',
        'platform/identity',
        'platform/persistence/aggregator',
        'platform/persistence/local',
        'platform/persistence/queue',
        'platform/policy',
        'platform/entanglement',
        'platform/search',
        'platform/status',
        'platform/commonUI/regions'
    ];

    DEFAULTS.forEach(function (bundlePath) {
        legacyRegistry.enable(bundlePath);
    });

    return legacyRegistry;
});