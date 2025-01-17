import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, Router } from '@angular/router';
import { RouterTestingModule } from '@angular/router/testing';
import { of } from 'rxjs';
import { Plan, Region } from 'src/app/types';

import { MaterialModule } from '../material/material.module';
import { AuthService, PlanService } from '../services';
import { PlanMapComponent } from './plan-map/plan-map.component';
import { PlanOverviewComponent } from './plan-summary/plan-overview/plan-overview.component';
import { PlanComponent } from './plan.component';
import { PlanModule } from './plan.module';

describe('PlanComponent', () => {
  let component: PlanComponent;
  let fixture: ComponentFixture<PlanComponent>;
  let mockAuthService: Partial<AuthService>;

  const fakeGeoJson: GeoJSON.GeoJSON = {
    type: 'FeatureCollection',
    features: [
      {
        type: 'Feature',
        geometry: {
          type: 'MultiPolygon',
          coordinates: [
            [
              [
                [10, 20],
                [10, 30],
                [15, 15],
              ],
            ],
          ],
        },
        properties: {
          shape_name: 'Test',
        },
      },
    ],
  };

  const fakePlan: Plan = {
    id: '24',
    name: 'somePlan',
    ownerId: 'owner',
    region: Region.SIERRA_NEVADA,
    planningArea: fakeGeoJson,
  };

  beforeEach(async () => {
    const fakeRoute = jasmine.createSpyObj(
      'ActivatedRoute',
      {},
      {
        snapshot: {
          paramMap: convertToParamMap({ id: '24' }),
        },
      }
    );

    mockAuthService = {};

    const fakeService = jasmine.createSpyObj('PlanService', {
      getPlan: of(fakePlan),
      getProjectsForPlan: of([]),
      updateStateWithPlan: of(),
      updateStateWithScenario: of(),
      updateStateWithConfig: of(),
      getScenariosForPlan: of([]),
      updateStateWithShapes: of([]),
    });
    fakeService.planState$ = of({});

    await TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
        MaterialModule,
        PlanModule,
        RouterTestingModule.withRoutes([]),
      ],
      declarations: [PlanComponent, PlanMapComponent, PlanOverviewComponent],
      providers: [
        { provide: ActivatedRoute, useValue: fakeRoute },
        { provide: AuthService, useValue: mockAuthService },
        { provide: PlanService, useValue: fakeService },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(PlanComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('fetches plan from service using ID', () => {
    expect(component.planNotFound).toBeFalse();
    expect(component.plan).toEqual(fakePlan);
  });

  it('calls service to update plan state based on route', () => {
    const planService = fixture.debugElement.injector.get(PlanService);

    expect(planService.updateStateWithPlan).toHaveBeenCalledOnceWith('24');
    expect(component.showOverview$.value).toBeTrue();
  });

  it('backToOverview navigates back to overview', () => {
    const router = fixture.debugElement.injector.get(Router);
    spyOn(router, 'navigate');

    component.backToOverview();

    expect(router.navigate).toHaveBeenCalledOnceWith(['plan', '24']);
  });
});
